from dotmap import DotMap

def dot(data, compile_to=None, data_type=str):
    # compile to: {1}[{:}]
    # string dot.notation
    notation_list = data.split('.')

    if isinstance(compile_to, str):
        # compiler = compile_to.replace('{1}', notation_list[0])
        compiling = ""
        compiling += notation_list[0]
        for notation in notation_list[1:]:
            # print('compiler is', compiler)
            
            dot_split = compile_to.replace('{1}', '').split('{.}')
            before = dot_split[0]
            after = dot_split[1]
            compiling += before
            compiling += notation
            compiling += after
            
            # print('before is', before, 'after is', after)
            # compiler = compiler.replace('{.}', notation)
        return compiling

def test_dot():
    assert dot('hey.dot', compile_to="{1}[{.}]") == "hey[dot]"
    assert dot('hey.dot.another', compile_to="{1}[{.}]") == "hey[dot][another]"
    assert dot('hey.dot.another.and.another', compile_to="{1}[{.}]") == "hey[dot][another][and][another]"
    assert dot('hey.dot', compile_to="{1}/{.}") == "hey/dot"
    assert dot('hey.dot.another', compile_to="{1}/{.}") == "hey/dot/another"
    assert dot('hey.dot.another', compile_to="{1}/{.}") == "hey/dot/another"
    dic = DotMap({'hey': {'dot': 'value'}})
    assert dic.hey.dot == 'value'
