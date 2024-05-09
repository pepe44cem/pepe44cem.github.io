package mx.itesm.aplicacion_comedor.model.bd_local


import androidx.room.Dao
import androidx.room.Insert

//Aqu
@Dao
interface UsuariosTotalesDAO {
    @Insert
    fun insertarUsuario(vararg usuario: BDLUsuarioTotales)
}