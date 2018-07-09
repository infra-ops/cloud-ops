CREATE MULTISET VOLATILE TABLE vt_acr131_fcr131_decision
, NO FALLBACK, NO JOURNAL, NO LOG(
batch_seq         int           null,
dec_key           bigint        not null,
dec_dt            date          not null,
run_dt            date          not null,
model             varchar(32)   not null,
dec_desc          varchar(32)   not null,
act_desc          varchar(32)   not null,
dec_key_scram     bigint        null,
dec_key_scram_desc      VARCHAR(128) null
)PRIMARY INDEX (dec_key)  
on commit preserve rows;

