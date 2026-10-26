# Independent helper review and corrections

An independent agent reviewed the state helper, state contract, installer, library checker,
and existing tests. The reviewer reproduced these findings with temporary synthetic records.
The integration agent made and tested the corrections.

| Finding | Correction | Regression evidence |
| --- | --- | --- |
| Changing only the target name could reuse a passing run with the same version label | Included project target identity in the contract fingerprint | `test_different_target_with_same_version_invalidates_previous_run` |
| Malformed optional resolution evidence on open/deferred gaps could raise an uncaught TypeError | Validate the known optional field whenever present, with nonempty content required for resolved gaps | `test_optional_resolution_evidence_is_validated_for_open_gaps` |
| Documentation said extra fields never affected the gate, while fingerprinted records include them | Documented conservative invalidation; fixture metadata in scenarios participates in freshness | `test_scenario_fixture_digest_change_invalidates_previous_run` |

The integration review also guarded against installing into a directory nested inside a
source skill, which could recursively copy the staging directory. The installer now refuses
that destination before writing. `test_destination_inside_source_is_rejected_before_recursive_copy`
covers the boundary.

The mounted source files reported mode 0777. The installer now normalizes new POSIX skill
files/directories so group/world write permission is not propagated; a regression test
checks that boundary.

All 35 state/installation tests passed after these changes. These tests validate concrete
helper behaviors; synthetic PASS records used as fixtures are not presented as real product
verification. The review did not establish record authenticity or comprehensive requirements.
