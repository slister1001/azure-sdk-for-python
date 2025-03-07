# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from ._data_masking_policies_operations import DataMaskingPoliciesOperations
from ._data_masking_rules_operations import DataMaskingRulesOperations
from ._geo_backup_policies_operations import GeoBackupPoliciesOperations
from ._databases_operations import DatabasesOperations
from ._elastic_pools_operations import ElasticPoolsOperations
from ._server_communication_links_operations import ServerCommunicationLinksOperations
from ._service_objectives_operations import ServiceObjectivesOperations
from ._elastic_pool_activities_operations import ElasticPoolActivitiesOperations
from ._elastic_pool_database_activities_operations import ElasticPoolDatabaseActivitiesOperations
from ._server_usages_operations import ServerUsagesOperations
from ._database_advisors_operations import DatabaseAdvisorsOperations
from ._database_automatic_tuning_operations import DatabaseAutomaticTuningOperations
from ._database_columns_operations import DatabaseColumnsOperations
from ._database_recommended_actions_operations import DatabaseRecommendedActionsOperations
from ._database_schemas_operations import DatabaseSchemasOperations
from ._database_security_alert_policies_operations import DatabaseSecurityAlertPoliciesOperations
from ._database_tables_operations import DatabaseTablesOperations
from ._database_vulnerability_assessment_rule_baselines_operations import (
    DatabaseVulnerabilityAssessmentRuleBaselinesOperations,
)
from ._database_vulnerability_assessments_operations import DatabaseVulnerabilityAssessmentsOperations
from ._database_vulnerability_assessment_scans_operations import DatabaseVulnerabilityAssessmentScansOperations
from ._data_warehouse_user_activities_operations import DataWarehouseUserActivitiesOperations
from ._deleted_servers_operations import DeletedServersOperations
from ._elastic_pool_operations_operations import ElasticPoolOperationsOperations
from ._encryption_protectors_operations import EncryptionProtectorsOperations
from ._firewall_rules_operations import FirewallRulesOperations
from ._job_agents_operations import JobAgentsOperations
from ._job_credentials_operations import JobCredentialsOperations
from ._job_executions_operations import JobExecutionsOperations
from ._job_private_endpoints_operations import JobPrivateEndpointsOperations
from ._jobs_operations import JobsOperations
from ._job_step_executions_operations import JobStepExecutionsOperations
from ._job_steps_operations import JobStepsOperations
from ._job_target_executions_operations import JobTargetExecutionsOperations
from ._job_target_groups_operations import JobTargetGroupsOperations
from ._job_versions_operations import JobVersionsOperations
from ._capabilities_operations import CapabilitiesOperations
from ._maintenance_window_options_operations import MaintenanceWindowOptionsOperations
from ._maintenance_windows_operations import MaintenanceWindowsOperations
from ._managed_backup_short_term_retention_policies_operations import ManagedBackupShortTermRetentionPoliciesOperations
from ._managed_database_columns_operations import ManagedDatabaseColumnsOperations
from ._managed_database_queries_operations import ManagedDatabaseQueriesOperations
from ._managed_database_schemas_operations import ManagedDatabaseSchemasOperations
from ._managed_database_security_alert_policies_operations import ManagedDatabaseSecurityAlertPoliciesOperations
from ._managed_database_security_events_operations import ManagedDatabaseSecurityEventsOperations
from ._managed_database_tables_operations import ManagedDatabaseTablesOperations
from ._managed_database_transparent_data_encryption_operations import ManagedDatabaseTransparentDataEncryptionOperations
from ._managed_database_vulnerability_assessment_rule_baselines_operations import (
    ManagedDatabaseVulnerabilityAssessmentRuleBaselinesOperations,
)
from ._managed_database_vulnerability_assessments_operations import ManagedDatabaseVulnerabilityAssessmentsOperations
from ._managed_database_vulnerability_assessment_scans_operations import (
    ManagedDatabaseVulnerabilityAssessmentScansOperations,
)
from ._managed_instance_administrators_operations import ManagedInstanceAdministratorsOperations
from ._managed_instance_azure_ad_only_authentications_operations import (
    ManagedInstanceAzureADOnlyAuthenticationsOperations,
)
from ._managed_instance_encryption_protectors_operations import ManagedInstanceEncryptionProtectorsOperations
from ._managed_instance_keys_operations import ManagedInstanceKeysOperations
from ._managed_instance_long_term_retention_policies_operations import (
    ManagedInstanceLongTermRetentionPoliciesOperations,
)
from ._managed_instance_operations_operations import ManagedInstanceOperationsOperations
from ._managed_instance_private_endpoint_connections_operations import (
    ManagedInstancePrivateEndpointConnectionsOperations,
)
from ._managed_instance_private_link_resources_operations import ManagedInstancePrivateLinkResourcesOperations
from ._managed_instance_tde_certificates_operations import ManagedInstanceTdeCertificatesOperations
from ._managed_instance_vulnerability_assessments_operations import ManagedInstanceVulnerabilityAssessmentsOperations
from ._managed_restorable_dropped_database_backup_short_term_retention_policies_operations import (
    ManagedRestorableDroppedDatabaseBackupShortTermRetentionPoliciesOperations,
)
from ._managed_server_security_alert_policies_operations import ManagedServerSecurityAlertPoliciesOperations
from ._operations import Operations
from ._private_endpoint_connections_operations import PrivateEndpointConnectionsOperations
from ._private_link_resources_operations import PrivateLinkResourcesOperations
from ._recoverable_managed_databases_operations import RecoverableManagedDatabasesOperations
from ._restore_points_operations import RestorePointsOperations
from ._server_advisors_operations import ServerAdvisorsOperations
from ._server_automatic_tuning_operations import ServerAutomaticTuningOperations
from ._server_azure_ad_administrators_operations import ServerAzureADAdministratorsOperations
from ._server_azure_ad_only_authentications_operations import ServerAzureADOnlyAuthenticationsOperations
from ._server_dev_ops_audit_settings_operations import ServerDevOpsAuditSettingsOperations
from ._server_dns_aliases_operations import ServerDnsAliasesOperations
from ._server_keys_operations import ServerKeysOperations
from ._server_operations_operations import ServerOperationsOperations
from ._server_security_alert_policies_operations import ServerSecurityAlertPoliciesOperations
from ._server_trust_groups_operations import ServerTrustGroupsOperations
from ._server_vulnerability_assessments_operations import ServerVulnerabilityAssessmentsOperations
from ._sql_agent_operations import SqlAgentOperations
from ._subscription_usages_operations import SubscriptionUsagesOperations
from ._sync_agents_operations import SyncAgentsOperations
from ._sync_groups_operations import SyncGroupsOperations
from ._sync_members_operations import SyncMembersOperations
from ._tde_certificates_operations import TdeCertificatesOperations
from ._time_zones_operations import TimeZonesOperations
from ._virtual_network_rules_operations import VirtualNetworkRulesOperations
from ._workload_classifiers_operations import WorkloadClassifiersOperations
from ._workload_groups_operations import WorkloadGroupsOperations
from ._backup_short_term_retention_policies_operations import BackupShortTermRetentionPoliciesOperations
from ._database_extensions_operations import DatabaseExtensionsOperations
from ._database_usages_operations import DatabaseUsagesOperations
from ._ledger_digest_uploads_operations import LedgerDigestUploadsOperations
from ._outbound_firewall_rules_operations import OutboundFirewallRulesOperations
from ._usages_operations import UsagesOperations
from ._long_term_retention_managed_instance_backups_operations import LongTermRetentionManagedInstanceBackupsOperations
from ._restorable_dropped_managed_databases_operations import RestorableDroppedManagedDatabasesOperations
from ._server_connection_policies_operations import ServerConnectionPoliciesOperations
from ._server_trust_certificates_operations import ServerTrustCertificatesOperations
from ._endpoint_certificates_operations import EndpointCertificatesOperations
from ._managed_database_sensitivity_labels_operations import ManagedDatabaseSensitivityLabelsOperations
from ._managed_database_recommended_sensitivity_labels_operations import (
    ManagedDatabaseRecommendedSensitivityLabelsOperations,
)
from ._sensitivity_labels_operations import SensitivityLabelsOperations
from ._recommended_sensitivity_labels_operations import RecommendedSensitivityLabelsOperations
from ._server_blob_auditing_policies_operations import ServerBlobAuditingPoliciesOperations
from ._database_blob_auditing_policies_operations import DatabaseBlobAuditingPoliciesOperations
from ._extended_database_blob_auditing_policies_operations import ExtendedDatabaseBlobAuditingPoliciesOperations
from ._extended_server_blob_auditing_policies_operations import ExtendedServerBlobAuditingPoliciesOperations
from ._database_advanced_threat_protection_settings_operations import DatabaseAdvancedThreatProtectionSettingsOperations
from ._server_advanced_threat_protection_settings_operations import ServerAdvancedThreatProtectionSettingsOperations
from ._managed_server_dns_aliases_operations import ManagedServerDnsAliasesOperations
from ._managed_database_advanced_threat_protection_settings_operations import (
    ManagedDatabaseAdvancedThreatProtectionSettingsOperations,
)
from ._managed_instance_advanced_threat_protection_settings_operations import (
    ManagedInstanceAdvancedThreatProtectionSettingsOperations,
)
from ._managed_database_move_operations_operations import ManagedDatabaseMoveOperationsOperations
from ._managed_instance_dtcs_operations import ManagedInstanceDtcsOperations
from ._synapse_link_workspaces_operations import SynapseLinkWorkspacesOperations
from ._virtual_clusters_operations import VirtualClustersOperations
from ._instance_failover_groups_operations import InstanceFailoverGroupsOperations
from ._managed_database_restore_details_operations import ManagedDatabaseRestoreDetailsOperations
from ._database_encryption_protectors_operations import DatabaseEncryptionProtectorsOperations
from ._managed_databases_operations import ManagedDatabasesOperations
from ._managed_ledger_digest_uploads_operations import ManagedLedgerDigestUploadsOperations
from ._recoverable_databases_operations import RecoverableDatabasesOperations
from ._restorable_dropped_databases_operations import RestorableDroppedDatabasesOperations
from ._server_configuration_options_operations import ServerConfigurationOptionsOperations
from ._start_stop_managed_instance_schedules_operations import StartStopManagedInstanceSchedulesOperations
from ._transparent_data_encryptions_operations import TransparentDataEncryptionsOperations
from ._database_operations_operations import DatabaseOperationsOperations
from ._ipv6_firewall_rules_operations import IPv6FirewallRulesOperations
from ._sql_vulnerability_assessment_baseline_operations import SqlVulnerabilityAssessmentBaselineOperations
from ._sql_vulnerability_assessment_baselines_operations import SqlVulnerabilityAssessmentBaselinesOperations
from ._sql_vulnerability_assessment_execute_scan_operations import SqlVulnerabilityAssessmentExecuteScanOperations
from ._sql_vulnerability_assessment_rule_baseline_operations import SqlVulnerabilityAssessmentRuleBaselineOperations
from ._sql_vulnerability_assessment_rule_baselines_operations import SqlVulnerabilityAssessmentRuleBaselinesOperations
from ._sql_vulnerability_assessment_scan_result_operations import SqlVulnerabilityAssessmentScanResultOperations
from ._sql_vulnerability_assessment_scans_operations import SqlVulnerabilityAssessmentScansOperations
from ._sql_vulnerability_assessments_settings_operations import SqlVulnerabilityAssessmentsSettingsOperations
from ._sql_vulnerability_assessments_operations import SqlVulnerabilityAssessmentsOperations
from ._database_sql_vulnerability_assessment_baselines_operations import (
    DatabaseSqlVulnerabilityAssessmentBaselinesOperations,
)
from ._database_sql_vulnerability_assessment_execute_scan_operations import (
    DatabaseSqlVulnerabilityAssessmentExecuteScanOperations,
)
from ._database_sql_vulnerability_assessment_rule_baselines_operations import (
    DatabaseSqlVulnerabilityAssessmentRuleBaselinesOperations,
)
from ._database_sql_vulnerability_assessment_scan_result_operations import (
    DatabaseSqlVulnerabilityAssessmentScanResultOperations,
)
from ._database_sql_vulnerability_assessment_scans_operations import DatabaseSqlVulnerabilityAssessmentScansOperations
from ._database_sql_vulnerability_assessments_settings_operations import (
    DatabaseSqlVulnerabilityAssessmentsSettingsOperations,
)
from ._failover_groups_operations import FailoverGroupsOperations
from ._instance_pools_operations import InstancePoolsOperations
from ._long_term_retention_backups_operations import LongTermRetentionBackupsOperations
from ._long_term_retention_policies_operations import LongTermRetentionPoliciesOperations
from ._managed_instances_operations import ManagedInstancesOperations
from ._servers_operations import ServersOperations
from ._replication_links_operations import ReplicationLinksOperations
from ._distributed_availability_groups_operations import DistributedAvailabilityGroupsOperations

from ._patch import __all__ as _patch_all
from ._patch import *  # pylint: disable=unused-wildcard-import
from ._patch import patch_sdk as _patch_sdk

__all__ = [
    "DataMaskingPoliciesOperations",
    "DataMaskingRulesOperations",
    "GeoBackupPoliciesOperations",
    "DatabasesOperations",
    "ElasticPoolsOperations",
    "ServerCommunicationLinksOperations",
    "ServiceObjectivesOperations",
    "ElasticPoolActivitiesOperations",
    "ElasticPoolDatabaseActivitiesOperations",
    "ServerUsagesOperations",
    "DatabaseAdvisorsOperations",
    "DatabaseAutomaticTuningOperations",
    "DatabaseColumnsOperations",
    "DatabaseRecommendedActionsOperations",
    "DatabaseSchemasOperations",
    "DatabaseSecurityAlertPoliciesOperations",
    "DatabaseTablesOperations",
    "DatabaseVulnerabilityAssessmentRuleBaselinesOperations",
    "DatabaseVulnerabilityAssessmentsOperations",
    "DatabaseVulnerabilityAssessmentScansOperations",
    "DataWarehouseUserActivitiesOperations",
    "DeletedServersOperations",
    "ElasticPoolOperationsOperations",
    "EncryptionProtectorsOperations",
    "FirewallRulesOperations",
    "JobAgentsOperations",
    "JobCredentialsOperations",
    "JobExecutionsOperations",
    "JobPrivateEndpointsOperations",
    "JobsOperations",
    "JobStepExecutionsOperations",
    "JobStepsOperations",
    "JobTargetExecutionsOperations",
    "JobTargetGroupsOperations",
    "JobVersionsOperations",
    "CapabilitiesOperations",
    "MaintenanceWindowOptionsOperations",
    "MaintenanceWindowsOperations",
    "ManagedBackupShortTermRetentionPoliciesOperations",
    "ManagedDatabaseColumnsOperations",
    "ManagedDatabaseQueriesOperations",
    "ManagedDatabaseSchemasOperations",
    "ManagedDatabaseSecurityAlertPoliciesOperations",
    "ManagedDatabaseSecurityEventsOperations",
    "ManagedDatabaseTablesOperations",
    "ManagedDatabaseTransparentDataEncryptionOperations",
    "ManagedDatabaseVulnerabilityAssessmentRuleBaselinesOperations",
    "ManagedDatabaseVulnerabilityAssessmentsOperations",
    "ManagedDatabaseVulnerabilityAssessmentScansOperations",
    "ManagedInstanceAdministratorsOperations",
    "ManagedInstanceAzureADOnlyAuthenticationsOperations",
    "ManagedInstanceEncryptionProtectorsOperations",
    "ManagedInstanceKeysOperations",
    "ManagedInstanceLongTermRetentionPoliciesOperations",
    "ManagedInstanceOperationsOperations",
    "ManagedInstancePrivateEndpointConnectionsOperations",
    "ManagedInstancePrivateLinkResourcesOperations",
    "ManagedInstanceTdeCertificatesOperations",
    "ManagedInstanceVulnerabilityAssessmentsOperations",
    "ManagedRestorableDroppedDatabaseBackupShortTermRetentionPoliciesOperations",
    "ManagedServerSecurityAlertPoliciesOperations",
    "Operations",
    "PrivateEndpointConnectionsOperations",
    "PrivateLinkResourcesOperations",
    "RecoverableManagedDatabasesOperations",
    "RestorePointsOperations",
    "ServerAdvisorsOperations",
    "ServerAutomaticTuningOperations",
    "ServerAzureADAdministratorsOperations",
    "ServerAzureADOnlyAuthenticationsOperations",
    "ServerDevOpsAuditSettingsOperations",
    "ServerDnsAliasesOperations",
    "ServerKeysOperations",
    "ServerOperationsOperations",
    "ServerSecurityAlertPoliciesOperations",
    "ServerTrustGroupsOperations",
    "ServerVulnerabilityAssessmentsOperations",
    "SqlAgentOperations",
    "SubscriptionUsagesOperations",
    "SyncAgentsOperations",
    "SyncGroupsOperations",
    "SyncMembersOperations",
    "TdeCertificatesOperations",
    "TimeZonesOperations",
    "VirtualNetworkRulesOperations",
    "WorkloadClassifiersOperations",
    "WorkloadGroupsOperations",
    "BackupShortTermRetentionPoliciesOperations",
    "DatabaseExtensionsOperations",
    "DatabaseUsagesOperations",
    "LedgerDigestUploadsOperations",
    "OutboundFirewallRulesOperations",
    "UsagesOperations",
    "LongTermRetentionManagedInstanceBackupsOperations",
    "RestorableDroppedManagedDatabasesOperations",
    "ServerConnectionPoliciesOperations",
    "ServerTrustCertificatesOperations",
    "EndpointCertificatesOperations",
    "ManagedDatabaseSensitivityLabelsOperations",
    "ManagedDatabaseRecommendedSensitivityLabelsOperations",
    "SensitivityLabelsOperations",
    "RecommendedSensitivityLabelsOperations",
    "ServerBlobAuditingPoliciesOperations",
    "DatabaseBlobAuditingPoliciesOperations",
    "ExtendedDatabaseBlobAuditingPoliciesOperations",
    "ExtendedServerBlobAuditingPoliciesOperations",
    "DatabaseAdvancedThreatProtectionSettingsOperations",
    "ServerAdvancedThreatProtectionSettingsOperations",
    "ManagedServerDnsAliasesOperations",
    "ManagedDatabaseAdvancedThreatProtectionSettingsOperations",
    "ManagedInstanceAdvancedThreatProtectionSettingsOperations",
    "ManagedDatabaseMoveOperationsOperations",
    "ManagedInstanceDtcsOperations",
    "SynapseLinkWorkspacesOperations",
    "VirtualClustersOperations",
    "InstanceFailoverGroupsOperations",
    "ManagedDatabaseRestoreDetailsOperations",
    "DatabaseEncryptionProtectorsOperations",
    "ManagedDatabasesOperations",
    "ManagedLedgerDigestUploadsOperations",
    "RecoverableDatabasesOperations",
    "RestorableDroppedDatabasesOperations",
    "ServerConfigurationOptionsOperations",
    "StartStopManagedInstanceSchedulesOperations",
    "TransparentDataEncryptionsOperations",
    "DatabaseOperationsOperations",
    "IPv6FirewallRulesOperations",
    "SqlVulnerabilityAssessmentBaselineOperations",
    "SqlVulnerabilityAssessmentBaselinesOperations",
    "SqlVulnerabilityAssessmentExecuteScanOperations",
    "SqlVulnerabilityAssessmentRuleBaselineOperations",
    "SqlVulnerabilityAssessmentRuleBaselinesOperations",
    "SqlVulnerabilityAssessmentScanResultOperations",
    "SqlVulnerabilityAssessmentScansOperations",
    "SqlVulnerabilityAssessmentsSettingsOperations",
    "SqlVulnerabilityAssessmentsOperations",
    "DatabaseSqlVulnerabilityAssessmentBaselinesOperations",
    "DatabaseSqlVulnerabilityAssessmentExecuteScanOperations",
    "DatabaseSqlVulnerabilityAssessmentRuleBaselinesOperations",
    "DatabaseSqlVulnerabilityAssessmentScanResultOperations",
    "DatabaseSqlVulnerabilityAssessmentScansOperations",
    "DatabaseSqlVulnerabilityAssessmentsSettingsOperations",
    "FailoverGroupsOperations",
    "InstancePoolsOperations",
    "LongTermRetentionBackupsOperations",
    "LongTermRetentionPoliciesOperations",
    "ManagedInstancesOperations",
    "ServersOperations",
    "ReplicationLinksOperations",
    "DistributedAvailabilityGroupsOperations",
]
__all__.extend([p for p in _patch_all if p not in __all__])
_patch_sdk()
