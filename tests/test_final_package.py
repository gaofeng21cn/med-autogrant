from __future__ import annotations

import unittest

from final_package.test_artifact_bundle_contract_cases import TestFinalPackageArtifactBundleContractCases
from final_package.test_artifact_list_cases import TestFinalPackageArtifactListCases
from final_package.test_artifact_object_cases import TestFinalPackageArtifactObjectCases
from final_package.test_build_cases import TestFinalPackageBuildCases
from final_package.test_output_identity_cases import TestFinalPackageOutputIdentityCases


__all__ = [
    "TestFinalPackageArtifactBundleContractCases",
    "TestFinalPackageArtifactListCases",
    "TestFinalPackageArtifactObjectCases",
    "TestFinalPackageBuildCases",
    "TestFinalPackageOutputIdentityCases",
]


if __name__ == "__main__":
    unittest.main()
