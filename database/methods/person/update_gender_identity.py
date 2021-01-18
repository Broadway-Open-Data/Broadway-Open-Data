

# database models
from database.models.people.person import Person
from database.models.people.gender_identity import GenderIdentity


# --------------------------------------------------------------------------------



def update_gender_identity(self, op, value):
    """
    Will update a person's gender identity. (This should work for racial identity too...)

    Pass an instance of 'Person' to 'self'

    Params:
        op: (str) Operation. Either "equal" or "append"
            "equal" --> will assert that this person's gender identity matches provided value(s)
            "append" --> will add if this person's gender identity doesn't contain the provided value(s)
        value: (str|list) either a string or a list of values
    """

    # make sure the operation is valid
    assert op in ('equal', 'append',)

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # if a string, convert to a tuple
    if isinstance(value, (str)):
        value = (value, )

    need_to_commit = False

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    if op=='equal':
        # add the gender identity
        for x in value:
            if x not in self.gender_identity:
                my_gender_id = GenderIdentity.get_or_create({'name':x.lower()})
                self._gender_identity.append(my_gender_id)
                need_to_commit = True

        for x in self.gender_identity:
            if x not in value:
                self.gender_identity.remove(x)
                need_to_commit = True
        # finally, commit
        if need_to_commit:
            session.commit()

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # otherwise
    elif op=='append':
        # add if you need to add
        for x in value:
            if x not in self.gender_identity:
                my_gender_id = GenderIdentity.get_or_create({'name':x.lower()})
                self._gender_identity.append(my_gender_id)
                need_to_commit = True
        # That's all
        if need_to_commit:
            session.commit()

    # No other choices
    # Done

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
