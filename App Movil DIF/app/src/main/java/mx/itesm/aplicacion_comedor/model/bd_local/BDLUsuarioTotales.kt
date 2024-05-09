package mx.itesm.aplicacion_comedor.model.bd_local

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity
data class BDLUsuarioTotales(
    @PrimaryKey(autoGenerate = true) val idUsuario: Int,
    @ColumnInfo(name = "codigo") val codigo: String?,
    @ColumnInfo(name = "curp") val curp: String?
)