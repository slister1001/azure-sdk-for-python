# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) Python Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from ._operations import StorageClassOperations
from ._operations import Operations
from ._operations import LoadBalancersOperations
from ._operations import BgpPeersOperations
from ._operations import ServicesOperations

from ._patch import __all__ as _patch_all
from ._patch import *  # pylint: disable=unused-wildcard-import
from ._patch import patch_sdk as _patch_sdk

__all__ = [
    "StorageClassOperations",
    "Operations",
    "LoadBalancersOperations",
    "BgpPeersOperations",
    "ServicesOperations",
]
__all__.extend([p for p in _patch_all if p not in __all__])
_patch_sdk()
