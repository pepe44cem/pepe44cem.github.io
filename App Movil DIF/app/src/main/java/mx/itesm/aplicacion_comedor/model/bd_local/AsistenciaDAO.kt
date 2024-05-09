package mx.itesm.aplicacion_comedor.model.bd_local

import androidx.room.Dao
import androidx.room.Insert

@Dao
interface AsistenciaDAO {
    @Insert
    fun insertarAsistencia(vararg usuario: BDLAsistencia)
}