import sqlalchemy as sa

from backend.common.model import MappedBase

sys_user_role = sa.Table(
    'sys_user_role',
    MappedBase.metadata,
    sa.Column('id', sa.BigInteger, primary_key=True, unique=True, index=True, autoincrement=True, comment='Primary key ID'),
    sa.Column(
        'user_id', sa.BigInteger, sa.ForeignKey('sys_user.id', ondelete='CASCADE'), primary_key=True, comment='User ID'
    ),
    sa.Column(
        'role_id', sa.BigInteger, sa.ForeignKey('sys_role.id', ondelete='CASCADE'), primary_key=True, comment='Role ID'
    ),
)

sys_role_menu = sa.Table(
    'sys_role_menu',
    MappedBase.metadata,
    sa.Column('id', sa.BigInteger, primary_key=True, unique=True, index=True, autoincrement=True, comment='Primary key ID'),
    sa.Column(
        'role_id', sa.BigInteger, sa.ForeignKey('sys_role.id', ondelete='CASCADE'), primary_key=True, comment='Role ID'
    ),
    sa.Column(
        'menu_id', sa.BigInteger, sa.ForeignKey('sys_menu.id', ondelete='CASCADE'), primary_key=True, comment='Menu ID'
    ),
)

sys_role_data_scope = sa.Table(
    'sys_role_data_scope',
    MappedBase.metadata,
    sa.Column('id', sa.BigInteger, primary_key=True, unique=True, index=True, autoincrement=True, comment='Primary key ID'),
    sa.Column(
        'role_id', sa.BigInteger, sa.ForeignKey('sys_role.id', ondelete='CASCADE'), primary_key=True, comment='Role ID'
    ),
    sa.Column(
        'data_scope_id',
        sa.BigInteger,
        sa.ForeignKey('sys_data_scope.id', ondelete='CASCADE'),
        primary_key=True,
        comment='Data scope ID',
    ),
)

sys_data_scope_rule = sa.Table(
    'sys_data_scope_rule',
    MappedBase.metadata,
    sa.Column('id', sa.BigInteger, primary_key=True, unique=True, index=True, autoincrement=True, comment='Primary key ID'),
    sa.Column(
        'data_scope_id',
        sa.BigInteger,
        sa.ForeignKey('sys_data_scope.id', ondelete='CASCADE'),
        primary_key=True,
        comment='Data scope ID',
    ),
    sa.Column(
        'data_rule_id',
        sa.BigInteger,
        sa.ForeignKey('sys_data_rule.id', ondelete='CASCADE'),
        primary_key=True,
        comment='Data rule ID',
    ),
)
