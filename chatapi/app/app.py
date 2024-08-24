import logging
import torch
from fastapi import Depends, FastAPI, HTTPException, Security
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoConfig
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file

# ログ設定
logging.basicConfig(level=logging.INFO)

# モデルとトークナイザーの設定
model_name = "elyza/Llama-3-ELYZA-JP-8B"
model_filenames = [
    "model-00001-of-00004.safetensors",
    "model-00002-of-00004.safetensors",
    "model-00003-of-00004.safetensors",
    "model-00004-of-00004.safetensors",
]
config_filename = "config.json"

# モデルと設定ファイルのダウンロード
model_file_paths = [hf_hub_download(model_name, filename, force_download=True) for filename in model_filenames]
config_file_path = hf_hub_download(model_name, config_filename, force_download=True)

# トークナイザーとモデルのロード
tokenizer = AutoTokenizer.from_pretrained(model_name)
config = AutoConfig.from_pretrained(config_file_path)

# safetensors ファイルをロードしてモデルを構築
model_state_dict = {}
for file_path in model_file_paths:
    model_state_dict.update(load_file(file_path))

model = AutoModelForCausalLM.from_config(config)
model.load_state_dict(model_state_dict)
model = model.to("cpu")  # モデルをCPUに移動
model.eval()  # モデルを評価モードに設定

# デフォルトのシステムプロンプト
DEFAULT_SYSTEM_PROMPT = "あなたは誠実で優秀な日本人のアシスタントです。特に指示が無い場合は、常に日本語で回答してください。"

# FastAPIアプリケーションのインスタンスを作成
app = FastAPI()

@app.get("/")
async def read_root(txt: str):

    print(f"AI Received: {txt}")

    # チャットテンプレートを適用
    messages = [
        {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
        {"role": "user", "content": txt},
    ]
    # プロンプトをトークナイザーでテンプレートに適用
    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    token_ids = tokenizer.encode(
        prompt, add_special_tokens=False, return_tensors="pt"
    )

    # attention_mask を設定
    attention_mask = torch.ones(token_ids.shape, dtype=torch.long)

    try:
        # 勾配計算を無効にしてモデルを実行
        with torch.no_grad():
            output_ids = model.generate(
                token_ids.to(model.device),
                attention_mask=attention_mask.to(model.device),
                max_new_tokens=1200,  # 生成する最大トークン数
                do_sample=True,  # サンプリングを有効にする
                temperature=0.6,  # 生成の多様性を制御する温度パラメータ
                top_p=0.9,  # トップPサンプリングの確率質量
                pad_token_id=tokenizer.eos_token_id,  # パディングトークンIDを設定
            )
        # 出力テンソルに異常な値が含まれていないかチェック
        if torch.isnan(output_ids).any() or torch.isinf(output_ids).any() or (output_ids < 0).any():
            raise ValueError("Generated output contains invalid values (inf, nan, or < 0).")
        # トークンIDをデコードしてテキストに変換
        output = tokenizer.decode(
            output_ids.tolist()[0][token_ids.size(1):], skip_special_tokens=True
        )
        print(f"AI Response : {output}")
        return {"response": output}
    except RuntimeError as e:
        # ランタイムエラーが発生した場合の処理
        raise HTTPException(status_code=500, detail=f"Runtime error: {e}")
    except ValueError as e:
        # 値エラーが発生した場合の処理
        raise HTTPException(status_code=500, detail=f"Value error: {e}")
