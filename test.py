from databases import models

x = models.Person(
    f_name="James",
    m_name="F.",
    l_name="Buckley"
)

print(x.gender_identity)
print("*"+x.full_name+"*")


for c in models.Person.__table__.columns:
    print(c.type)
