from typing import List

import httpx
from pydantic import BaseModel

from app.core.config import settings


class UserProfile(BaseModel):
    id: int
    name: str
    roles: List[str]

    async def has_any_role(self, role_list: List[str], include_parents=False, include_children=False) -> bool:
        """权限验证方法，判断当前用户是否拥有指定角色（中的一个）

        Args:
            role_list:要求当前用户拥有的角色列表，满足其一即可
            include_parents:判断时是否包含当前用户拥有角色的所有父角色
            include_children:判断时是否包含当前用户拥有角色的所有子角色

        Returns:布尔值

        """
        owned_roles = set()
        owned_roles.update(self.roles)

        if include_parents is True and self.roles:
            async with httpx.AsyncClient() as client:
                r = await client.get(f'http://{settings.USER_SERVER}/internal/roles/parents',
                                     params={'role': self.roles})
            r.raise_for_status()
            parent_roles = r.json()

            if isinstance(parent_roles, list):
                owned_roles.update(parent_roles)

        if include_children is True and self.roles:
            async with httpx.AsyncClient() as client:
                r = await client.get(f'http://{settings.USER_SERVER}/internal/roles/children',
                                     params={'role': self.roles})
            r.raise_for_status()
            child_roles = r.json()

            if isinstance(child_roles, list):
                owned_roles.update(child_roles)

        if '管理员' in owned_roles:
            return True

        for role in role_list:
            if role in owned_roles:
                return True

        return False

class AccessToken(BaseModel):
    access_token: str
    token_type: str