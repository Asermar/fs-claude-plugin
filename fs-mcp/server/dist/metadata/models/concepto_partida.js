// Archivo generado automáticamente por scripts/generate-metadata.ts
// No editar a mano: cualquier cambio se perderá al regenerar.
export const conceptoPartidaMetadata = {
    "name": "concepto_partida",
    "table": "conceptos_partidas",
    "endpoint": "/conceptopartidas",
    "primaryKey": "codconcepto",
    "description": "Concepto preconfigurado para acelerar la creación de partidas en asientos.",
    "source": "core",
    "columns": [
        {
            "name": "codconcepto",
            "sqlType": "character varying(6)",
            "tsType": "string",
            "nullable": false,
            "isPrimaryKey": true,
            "isReadonly": true,
            "isRequired": true,
            "label": "Código",
            "maxLength": 6,
            "description": "Código corto único del concepto preconfigurado.",
            "widget": "text"
        },
        {
            "name": "descripcion",
            "sqlType": "character varying(255)",
            "tsType": "string",
            "nullable": false,
            "isPrimaryKey": false,
            "isReadonly": false,
            "isRequired": true,
            "label": "Descripción",
            "maxLength": 255,
            "description": "Texto del concepto que se autocompletará en las partidas al usarlo.",
            "widget": "text"
        }
    ],
    "relations": [],
    "generatedFrom": {
        "generatedAt": "2026-10-06T17:52:38.200Z",
        "facturascriptsCommit": "93a6a74ac"
    }
};
export default conceptoPartidaMetadata;
//# sourceMappingURL=concepto_partida.js.map