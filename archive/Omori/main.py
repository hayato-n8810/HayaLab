import socsel

ast1 = socsel.parse_code('arr = arr.concat(arr2);')
ast2 = socsel.parse_code('arr.push(...arr2);')

diff = socsel.gumtree(ast1, ast2)
pattern = socsel.pattern_diff(diff)

ast3 = socsel.parse_code('a = a.concat(b); b = b.concat(c);')
for result in socsel.findall_pattern(pattern, ast3):
    print([ast3.code[min(n.begin for n in ast3.tree[b:e]) : max(n.end for n in ast3.tree[b:e])] for b, e in result])



