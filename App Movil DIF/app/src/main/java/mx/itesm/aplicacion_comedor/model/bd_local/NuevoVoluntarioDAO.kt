package mx.itesm.aplicacion_comedor.model.bd_local

import androidx.room.Dao
import androidx.room.Insert

//Aqu
@Dao
interface NuevoVoluntarioDAO {
    @Insert
    fun insertarUsuario(vararg usuario: BDLNuevoVoluntario)
}