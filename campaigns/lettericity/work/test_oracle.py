from check import legal_target,solve_target,valid_target


def test_hand_cases():
    edge = {"vertices":2,"edges":[[0,1]],"letters":1}
    assert valid_target(edge,{"order":[0,1],"labels":[0,0],"decoder":[[True]]})
    assert solve_target({**edge,"letters":0}) == {"status":"NO-SOLUTION"}
    assert not valid_target(edge,{"order":[0,1],"labels":[0,0],"decoder":[[False]]})
    assert not legal_target({"vertices":2,"edges":[[1,0]],"letters":1})
    mixed = {"vertices":3,"edges":[[0,1]],"letters":1}
    assert solve_target(mixed) == {"status":"NO-SOLUTION"}


if __name__ == "__main__":
    test_hand_cases()
