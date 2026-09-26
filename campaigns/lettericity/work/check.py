"""Independent 3-SAT and split-graph star-coloring oracles."""

import argparse
import json
import subprocess
import sys
from itertools import combinations, permutations, product
from pathlib import Path

import z3


def legal_source(source):
    if not isinstance(source, dict):
        return False
    n = source.get("num_vars")
    clauses = source.get("clauses")
    return (type(n) is int and n >= 0 and isinstance(clauses, list)
            and all(isinstance(clause, list) and len(clause) <= 3
                    and all(type(literal) is int and 1 <= abs(literal) <= n for literal in clause)
                    for clause in clauses))


def solve_source(source):
    if not legal_source(source):
        raise ValueError("Illegal source formula")
    variables = [z3.Bool(f"x{i}") for i in range(source["num_vars"])]
    solver = z3.Solver()
    for clause in source["clauses"]:
        solver.add(z3.Or(*(variables[abs(literal) - 1] if literal > 0
                           else z3.Not(variables[-literal - 1]) for literal in clause)))
    result = solver.check()
    if result == z3.unsat:
        return {"status": "NO-SOLUTION"}
    if result != z3.sat:
        raise RuntimeError(f"Inconclusive source solver: {result}")
    model = solver.model()
    return {"assignment": [z3.is_true(model.eval(variable, model_completion=True)) for variable in variables]}


def valid_source(source, output):
    if not legal_source(source) or not isinstance(output, dict):
        return False
    if output == {"status": "NO-SOLUTION"}:
        return solve_source(source) == output
    assignment = output.get("assignment")
    if set(output) != {"assignment"} or not isinstance(assignment, list) or len(assignment) != source["num_vars"] or any(type(value) is not bool for value in assignment):
        return False
    return all(any(assignment[abs(literal) - 1] == (literal > 0) for literal in clause)
               for clause in source["clauses"])


def legal_target(target):
    if not isinstance(target,dict) or set(target) != {"vertices","edges","letters"}:
        return False
    n,edges,k = target["vertices"],target["edges"],target["letters"]
    return (type(n) is int and n >= 0 and type(k) is int and k >= 0
            and isinstance(edges,list)
            and all(isinstance(edge,list) and len(edge) == 2
                    and all(type(v) is int and 0 <= v < n for v in edge)
                    and edge[0] < edge[1] for edge in edges)
            and len({tuple(edge) for edge in edges}) == len(edges))


def direct_representation(target,order,labels,decoder):
    n,k = target["vertices"],target["letters"]
    if (not isinstance(order,list) or sorted(order) != list(range(n))
            or any(type(v) is not int for v in order)
            or not isinstance(labels,list) or len(labels) != n
            or any(type(a) is not int or not 0 <= a < k for a in labels)
            or not isinstance(decoder,list) or len(decoder) != k
            or any(not isinstance(row,list) or len(row) != k
                    or any(type(bit) is not bool for bit in row) for row in decoder)):
        return False
    position = {v:i for i,v in enumerate(order)}
    edges = {tuple(edge) for edge in target["edges"]}
    for u in range(n):
        for v in range(u+1,n):
            first,second = (u,v) if position[u] < position[v] else (v,u)
            if decoder[labels[first]][labels[second]] != ((u,v) in edges):
                return False
    return True


def target_solutions(target,limit=3):
    if not legal_target(target):
        raise ValueError("Illegal lettericity instance")
    n,k = target["vertices"],target["letters"]
    pos = [z3.Int(f"pos_{v}") for v in range(n)]
    labels = [z3.Int(f"letter_{v}") for v in range(n)]
    decoder = z3.Array("decoder",z3.IntSort(),z3.BoolSort())
    solver = z3.Solver()
    if n:
        solver.add(z3.Distinct(pos))
    for p in pos:
        solver.add(p >= 0,p < n)
    for a in labels:
        solver.add(a >= 0,a < k)
    edges = {tuple(edge) for edge in target["edges"]}
    for u in range(n):
        for v in range(u+1,n):
            index = z3.If(pos[u] < pos[v],labels[u]*k+labels[v],labels[v]*k+labels[u])
            solver.add(z3.Select(decoder,index) == ((u,v) in edges))
    outputs = []
    while len(outputs) < limit:
        result = solver.check()
        if result == z3.unsat:
            break
        if result != z3.sat:
            raise RuntimeError(f"Inconclusive target solver: {result}")
        model = solver.model()
        positions = [model.eval(p).as_long() for p in pos]
        order = sorted(range(n),key=lambda v:positions[v])
        letters = [model.eval(a).as_long() for a in labels]
        table = [[z3.is_true(model.eval(z3.Select(decoder,i*k+j),model_completion=True))
                  for j in range(k)] for i in range(k)]
        assert direct_representation(target,order,letters,table)
        outputs.append({"order":order,"labels":letters,"decoder":table})
        block = [p != positions[v] for v,p in enumerate(pos)]
        block += [a != letters[v] for v,a in enumerate(labels)]
        block += [z3.Select(decoder,i*k+j) != table[i][j] for i in range(k) for j in range(k)]
        if not block:
            break
        solver.add(z3.Or(*block))
    return outputs or [{"status":"NO-SOLUTION"}]


def solve_target(target):
    return target_solutions(target,1)[0]


def valid_target(target,output):
    if not legal_target(target) or not isinstance(output,dict):
        return False
    if output == {"status":"NO-SOLUTION"}:
        return solve_target(target) == output
    return (set(output) == {"order","labels","decoder"}
            and direct_representation(target,output["order"],output["labels"],output["decoder"]))


def exhaustive_target(target):
    n,k = target["vertices"],target["letters"]
    edges = {tuple(edge) for edge in target["edges"]}
    for order in permutations(range(n)):
        position = {v:i for i,v in enumerate(order)}
        for labels in product(range(k),repeat=n):
            required = {}
            good = True
            for u in range(n):
                for v in range(u+1,n):
                    first,second = (u,v) if position[u] < position[v] else (v,u)
                    pair = labels[first],labels[second]
                    value = (u,v) in edges
                    if pair in required and required[pair] != value:
                        good = False
                        break
                    required[pair] = value
                if not good:
                    break
            if good:
                table = [[required.get((i,j),False) for j in range(k)] for i in range(k)]
                return {"order":list(order),"labels":list(labels),"decoder":table}
    return {"status":"NO-SOLUTION"}


def self_test():
    from generate_cases import EDGE_CASES,random_source
    from test_oracle import test_hand_cases
    root = Path(__file__).resolve().parents[3]
    path = Path(__file__).with_name("cases.json")
    subprocess.run([sys.executable,str(root/"research/validate_preparation.py"),str(path)],check=True,cwd=root)
    cases = json.loads(path.read_text())
    for n,clauses,answer in EDGE_CASES:
        assert ("assignment" in solve_source({"num_vars":n,"clauses":clauses})) == answer
    for case in cases:
        source = case["source"]
        if case["kind"] == "random":
            assert random_source(case["seed"]) == source
        current = solve_source(source)
        exists = any(all(any(bits[abs(lit)-1] == (lit > 0) for lit in clause)
                             for clause in source["clauses"])
                     for bits in product((False,True),repeat=source["num_vars"]))
        assert ("assignment" in current) == exists == ("assignment" in case["expected"])
        assert valid_source(source,current) and valid_source(source,case["expected"])
    test_hand_cases()
    checked = 0
    for n in range(5):
        slots = list(combinations(range(n),2))
        for mask in range(1 << len(slots)):
            edges = [list(edge) for i,edge in enumerate(slots) if mask & (1 << i)]
            for k in range(3):
                target = {"vertices":n,"edges":edges,"letters":k}
                assert ("order" in solve_target(target)) == ("order" in exhaustive_target(target))
                checked += 1
    print(f"Self-test passed: {len(cases)} source formulas and {checked} exhaustive graph-alphabet targets")


def candidate_check(path):
    self_test()
    cases = json.loads(Path(__file__).with_name("cases.json").read_text())
    recovered = 0
    for case in cases:
        source = case["source"]
        forward = subprocess.run([sys.executable,str(path)],input=json.dumps(source),text=True,capture_output=True,check=True)
        target = json.loads(forward.stdout)
        if not legal_target(target):
            raise AssertionError(f"Illegal target: {target}")
        for output in target_solutions(target):
            assert valid_target(target,output)
            payload = {"source":source,"target_solution":output}
            extraction = subprocess.run([sys.executable,str(path),"--extract"],input=json.dumps(payload),text=True,capture_output=True,check=True)
            recovered_output = json.loads(extraction.stdout)
            if not valid_source(source,recovered_output):
                raise AssertionError(f"Invalid recovery from {output}: {recovered_output}")
            recovered += 1
    print(f"Candidate check passed: {len(cases)} source cases, {recovered} target outputs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test",action="store_true")
    group.add_argument("--candidate",type=Path)
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        candidate_check(args.candidate)
