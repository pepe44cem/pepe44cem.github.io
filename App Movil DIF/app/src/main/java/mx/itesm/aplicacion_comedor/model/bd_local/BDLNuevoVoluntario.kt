package mx.itesm.aplicacion_comedor.model.bd_local

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity
data class BDLNuevoVoluntario(
    @PrimaryKey(autoGenerate = true) val idVoluntario: Int,
    @ColumnInfo(name = "nombreCompleto") val nombreCompleto: String?,
    @ColumnInfo(name = "curp") val curp: String?,
    @ColumnInfo(name = "telefono") val telefono: String?,
    @ColumnInfo(name = "estadoEnvio") val estadoEnvio: Boolean?
)
