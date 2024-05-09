package mx.itesm.aplicacion_comedor.model.bd_local

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity
data class BDLVisita(
    @PrimaryKey(autoGenerate = true) val idVisita: Int,
    @ColumnInfo(name = "codigoUsuario") val codigoUsuario: String?,
    @ColumnInfo(name = "usuarioComedor") val usuarioComedro: String?,
    @ColumnInfo(name = "fechaHora") val curp: String?,
    @ColumnInfo(name = "racionPagada") val racionPagada: Boolean?,
    @ColumnInfo(name = "donadoPor") val donadoPor: String?,
    @ColumnInfo(name = "estadoEnvio") val estadoEnvio: Boolean?
)
