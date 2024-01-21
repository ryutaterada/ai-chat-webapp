import logging
import torch
from fastapi import Depends, FastAPI, HTTPException, Security
from transformers import AutoModelForCausalLM, AutoTokenizer

B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
DEFAULT_SYSTEM_PROMPT = "あなたは誠実で優秀な日本人のアシスタントです。"

model_name = "elyza/ELYZA-japanese-Llama-2-7b-fast-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
model = model.to("cpu")

app = FastAPI()


@app.get("/")
async def read_root(txt: str):
    logging.info(f"Received text: {txt}")
    prompt = "{bos_token}{b_inst} {system}{prompt} {e_inst} ".format(
        bos_token=tokenizer.bos_token,
        b_inst=B_INST,
        system=f"{B_SYS}{DEFAULT_SYSTEM_PROMPT}{E_SYS}",
        prompt=txt,
        e_inst=E_INST,
    )

    with torch.no_grad():
        token_ids = tokenizer.encode(
            prompt, add_special_tokens=False, return_tensors="pt")

        output_ids = model.generate(
            token_ids.to(model.device),
            max_new_tokens=256,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )
    output = tokenizer.decode(
        output_ids.tolist()[0][token_ids.size(1):], skip_special_tokens=True)

    logging.info(f"Generated text: {output}")
    return output
