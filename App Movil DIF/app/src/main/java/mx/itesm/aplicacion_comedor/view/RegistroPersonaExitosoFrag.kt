package mx.itesm.aplicacion_comedor.view

import androidx.lifecycle.ViewModelProvider
import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import mx.itesm.aplicacion_comedor.R
import mx.itesm.aplicacion_comedor.viewmodel.RegistroPersonaExitosoVM

class RegistroPersonaExitosoFrag : Fragment() {

    companion object {
        fun newInstance() = RegistroPersonaExitosoFrag()
    }

    private lateinit var viewModel: RegistroPersonaExitosoVM

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_registro_persona_exitoso, container, false)
    }

    override fun onActivityCreated(savedInstanceState: Bundle?) {
        super.onActivityCreated(savedInstanceState)
        viewModel = ViewModelProvider(this).get(RegistroPersonaExitosoVM::class.java)
        // TODO: Use the ViewModel
    }

}