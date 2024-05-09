package mx.itesm.aplicacion_comedor.model.bd_local

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity
data class BDLNuevoUsuario(
    @PrimaryKey(autoGenerate = true) val idUsuario: Int,
    @ColumnInfo(name = "nombre") val nombre: String?,
    @ColumnInfo(name = "apellido") val apellido: String?,
    @ColumnInfo(name = "curp") val curp: String?,
    @ColumnInfo(name = "fechaNacimiento") val fechaNacimiento: String?,
    @ColumnInfo(name = "sexo") val sexo: String?,
    @ColumnInfo(name = "codigo") val codigo: String?,
    @ColumnInfo(name = "condicion") val condicion: String?,
    @ColumnInfo(name = "estadoEnvio") val estadoEnvio: Boolean?
)
