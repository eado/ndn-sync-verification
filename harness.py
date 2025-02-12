import os

class TestCase(object):
     __slots__= "msg_vector", "msg_increase", "current_vector", "current_state"

     def display(self):
        state = "STABLE" if getattr(self, "current_state") == 0 else "SUPPRESSION"
        msg = "Increase Sequence Number" if getattr(self, "msg_increase") else "Updated Vector: " + str(getattr(self, "msg_vector"))
        vector = str(getattr(self, "current_vector"))
        print(f"Current State: {state}")
        print(f"Current State Vector: {vector}")
        print(f"Recv Message: {msg}\n")

def cleanup():
    cwd = os.getcwd()
    generated = [
        "klee-last",
        "klee-out-0",
        "my_klee.bc",
        "results"
    ]

    for f in os.listdir(cwd):
        if f in generated:
            full = os.path.join(cwd,f)
            cmd = f"rm -r {full}"
            os.system(cmd)

def generate():
    cwd = os.getcwd()
    bc = f"cd {cwd} && clang -I ../../include -emit-llvm -c -g -O0 -Xclang -disable-O0-optnone my_klee.c"
    klee = f"cd {cwd} && klee my_klee.bc"
    os.system(bc)
    os.system(klee)

def fetch():
    cwd = os.getcwd()
    info = os.path.join(cwd,"results")
    os.mkdir(info)
    results = os.path.join(cwd,"klee-last")
    cmd = lambda t: f"cd {cwd} && ktest-tool klee-last/{t}.ktest > results/{t}.txt"
    for t in os.listdir(results):
        if t.endswith(".ktest"):
            c = cmd(t.removesuffix(".ktest"))
            os.system(c)

def read(filename):
    with open(filename) as f:
        return f.read()
          
def process():
    fields = [
        "\'current_state\'",
        "\'current_vector_5\'",
        "\'current_vector_4\'",
        "\'current_vector_3\'",
        "\'current_vector_2\'",
        "\'current_vector_1\'",
        "\'msg_vector_5\'",
        "\'msg_vector_4\'",
        "\'msg_vector_3\'",
        "\'msg_vector_2\'",
        "\'msg_vector_1\'",
        "\'msg_increase\'"
    ]
    tests = []
    cwd = os.getcwd()
    info = os.path.join(cwd,"results")
    for t in os.listdir(info):
        values = {}
        content = read(os.path.join(info,t))
        for group in content.split("name:"):
            sections = list(map(lambda s: s.strip(), group.split("object")))
            field = sections[0].strip()
            if field in fields:
                filtered = list(filter(lambda s: len(s.split(":")) == 3, sections))
                value = list(filter(lambda s: s.split(":")[1].strip() == "int", filtered))
                field_final = field.removeprefix("\'").removesuffix("\'")
                value_final = int(value[0].split(":")[2].strip())
                values[field_final] = value_final
        tests += [values] 
    return tests  

def format(test):
    t = TestCase()
    current_vector = [
        test["current_vector_1"],
        test["current_vector_2"],
        test["current_vector_3"],
        test["current_vector_4"],
        test["current_vector_5"]
    ]
    msg_vector = [
        test["msg_vector_1"],
        test["msg_vector_2"],
        test["msg_vector_3"],
        test["msg_vector_4"],
        test["msg_vector_5"]
    ]
    t.current_state = (test["current_state"])
    t.msg_increase = bool(test["current_state"])
    t.current_vector = current_vector
    t.msg_vector = msg_vector
    return t

def run():
    cleanup()
    generate()
    fetch()
    raw = process()
    tests = list(map(format,raw))
    for t in tests:
        t.display()
    cleanup()

run()