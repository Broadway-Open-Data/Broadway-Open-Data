# database models
from database.models.people.person import Person
from database.models.people.racial_identity import RacialIdentity


# --------------------------------------------------------------------------------


def update_racial_identity(self, op, value):
    """
    Will update a person's racial identity. (This is kind of a copy of updating
    racial identity. Not the best DRY code, but it works!)

    Pass an instance of 'Person' to 'self'

    Params:
        op: (str) Operation. Either "equal" or "append"
            "equal" --> will assert that this person's racial identity matches provided value(s)
            "append" --> will add if this person's racial identity doesn't contain the provided value(s)
        value: (str|list) either a string or a list of values
    """

    # make sure the operation is valid
    assert op in ('equal', 'append')

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # if a string, convert to a tuple
    if isinstance(value, (str)):
        value = (value, )

    need_to_commit = False

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    if op=='equal':
        # add the racial identity
        for x in value:
            if x not in self.racial_identity:
                my_racial_id = RacialIdentity.get_or_create({'name':x.lower()})
                self._racial_identity.append(my_racial_id)
                need_to_commit = True

        for x in self.racial_identity:
            if x not in value:
                self.racial_identity.remove(x)
                need_to_commit = True

        # finally, commit (if you need to)
        if need_to_commit:
            session.commit()

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # otherwise
    elif op=='append':
        # add if you need to add
        for x in value:
            if x not in self.racial_identity:
                my_racial_id = RacialIdentity.get_or_create({'name':x.lower()})
                self._racial_identity.append(my_racial_id)
                need_to_commit = True

        # That's all
        if need_to_commit:
            session.commit()

    # No other choices
    # Done

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
