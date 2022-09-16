from sqlalchemy import UniqueConstraint


account_unique_constraint = UniqueConstraint(
    "account", name="account_unique_constraint"
)
nickname_unique_constraint = UniqueConstraint(
    "nickname", name="nickname_unique_constraint"
)
family_name_unique_constraint = UniqueConstraint(
    "name", name="family_name_unique_constraint"
)
