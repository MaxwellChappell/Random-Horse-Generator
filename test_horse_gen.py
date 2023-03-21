import horse_gen
import itertools

print()
name  = "test"
color = "bay"
sex = "mare"
country = "US"
year = 1984
sire = "dad"
dam = "mom"
fail = "Not Recorded"
lst = list(itertools.product([0, 1], repeat=6))

for i in lst:
    things = [color, sex, country, year, sire, dam]
    things = [item if i[index]==1 else fail for index, item in enumerate(things)]
    print(things,horse_gen.create_story(name, *things),"", sep="\n")

