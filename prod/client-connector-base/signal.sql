-- Oracle
CREATE TABLE INTCDC.DEBEZIUM_SIGNAL (id VARCHAR(42) PRIMARY KEY, type VARCHAR(32) NOT NULL, data VARCHAR(2048) NULL);

ALTER TABLE INTCDC.DEBEZIUM_SIGNAL ADD SUPPLEMENTAL LOG DATA (ALL) COLUMNS;

INSERT
	INTO
	INTCDC.DEBEZIUM_SIGNAL
(ID,
	"TYPE",
	"DATA")
VALUES('ad-hoc-13',
'execute-snapshot',
'{"data-collections": ["ORCLCDB.SOURCE_C1.TB_9"],"type":"incremental"}');


--SqlServer
CREATE TABLE <schema>.debezium_signal (id VARCHAR(42) PRIMARY KEY, type VARCHAR(32) NOT NULL, data VARCHAR(2048) NULL);
EXEC sys.sp_cdc_enable_table @source_schema = '<source>', @source_name = 'debezium_signal', @role_name = NULL, @supports_net_changes = 0;

INSERT
	INTO
	dbo.debezium_signal
(ID,
	"TYPE",
	"DATA")
VALUES('ad-hoc-1',
'execute-snapshot',
'{"data-collections": ["dbo.orders"],"type":"incremental"}');

