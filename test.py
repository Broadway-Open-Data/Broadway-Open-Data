from databases import models

x = models.Person(
    f_name="James",
    m_name="F.",
    l_name="Buckley"
)


print("*"+x.full_name+"*")
