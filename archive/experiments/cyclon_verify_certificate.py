# Independent exact verification of the fixed-phase enhanced-CYCLON counterexample.
# Each cache contains (peer_id,age); exchanges here always involve three distinct IDs.
state=((3,0),(4,0),(2,0),(1,0))
initial=state
expected=[(2,4,1,1),(2,1,1,2),(3,1,2,2),(3,4,2,1)]
for p,want in zip(range(1,5),expected):
    q,oldage=state[p-1]
    r,response_age=state[q-1]
    assert len({p,q,r})==3
    new=list(state)
    new[p-1]=(r,response_age)
    new[q-1]=(p,0)
    state=tuple(new)
    assert tuple(j for j,a in state)==want
    assert all(a==0 for j,a in state)
assert state==initial
print('Verified exactly: four-step state cycle, all ages zero; no reciprocal-target exchange.')
