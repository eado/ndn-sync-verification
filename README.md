# Symbolic Test Generation for NDN (using LLM generated models)

## Files
* `prompt.txt` = prompt to LLM
* `llm-context.txt` = contains the context used as system prompt
* `gen_context.py` = file to generate system prompt context (using simple RAG)
* `gen_ndn_model.py` = file to query LLM (make sure `llm-context.txt` and `prompt.txt` are filled in)
* `ndn-context.txt` = text about NDN SVS
* `my_klee.py` = contains the model being used to symbolically generate tests and klee usage
* `harness.py` = python script to symbolically execute the models and format tests

## Order to Execute
(__Optional__) Generate Context

``` $ python gen_context.py > llm-context.txt```

Generate Model(s) -- make sure API key is filled in (in the `gen_ndn_model.py` file)

``` $ python gen_ndn_model.py > model.c```

Look at the output `model.c` and remove any text that is not the desired code, and paste the model in the "Example Model" portion of the `my_klee.c` file.

Run the symbolic execution and process the results

``` $ python harness.py > tests.txt ```