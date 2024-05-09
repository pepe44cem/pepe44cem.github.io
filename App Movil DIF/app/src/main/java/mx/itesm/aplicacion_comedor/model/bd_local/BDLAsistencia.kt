package mx.itesm.aplicacion_comedor.model.bd_local

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity
data class BDLAsistencia(
    @PrimaryKey(autoGenerate = true) val idAsistencia: Int,
    @ColumnInfo(name = "usuarioComedor") val usuarioComedor: String?,
    @ColumnInfo(name = "curpVoluntario") val curpVoluntario: String?,
    @ColumnInfo(name = "fechaHora") val fechaHora: String?,
    @ColumnInfo(name = "estadoEnvio") val estadoEnvio: Boolean?
)
