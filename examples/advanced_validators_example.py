def validator(value: int):
    # Values passed to validators already been casted using their caster so you don't have to worry about that
    # This is one of the ways to tell that something is wrong with value
    if value > 1024:
        raise ValueError("Too big number to handle")

    if value == 256:
        # This is also the way to show that something is wrong, but it not allowing you to tell what.
        # The only thing that will be told is what variable was invalid in which loader.
        return False

    # Also keep in mind that validators always must return bool value or it will not work properly in some cases
    return True
