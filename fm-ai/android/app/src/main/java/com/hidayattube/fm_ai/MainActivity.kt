package com.hidayattube.fm_ai

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.net.HttpURLConnection
import java.net.URL

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent { FmAiScreen() }
    }
}

@Composable
fun FmAiScreen() {
    val prefs = remember { context.getSharedPreferences("fm_ai_connection", Context.MODE_PRIVATE) }
    var baseUrl by remember { mutableStateOf(prefs.getString("fm_computer_url", "http://127.0.0.1:8080") ?: "http://127.0.0.1:8080") }
    var status by remember { mutableStateOf("Not checked") }
    var checking by remember { mutableStateOf(false) }
    var discovering by remember { mutableStateOf(false) }
    val scope = rememberCoroutineScope()

    Column(Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.spacedBy(16.dp)) {
        Text("FM AI", style = MaterialTheme.typography.headlineMedium)
        Text("Survival Computer AI • FM Computer connection")
        OutlinedTextField(
            value = baseUrl,
            onValueChange = { baseUrl = it.trimEnd('/') },
            label = { Text("FM Computer URL") },
            modifier = Modifier.fillMaxWidth(),
            singleLine = true
        )
        Button(enabled = !checking, onClick = {
            prefs.edit().putString("fm_computer_url", baseUrl).apply()
            checking = true
            status = "Checking…"
            scope.launch {
                status = healthCheck(baseUrl)
                checking = false
            }
        }) { Text("Check FM Computer") }
        Text(status)
        OutlinedButton(enabled = !discovering, onClick = {
            discovering = true
            status = "Searching local network…"
            discoverFmComputer(context) { discovered ->
                discovering = false
                if (discovered != null) {
                    baseUrl = discovered
                    prefs.edit().putString("fm_computer_url", discovered).apply()
                    status = "FM Computer found: " + discovered
                } else status = "FM Computer not found; enter its current LAN URL."
            }
        }) { Text(if (discovering) "Searching…" else "Auto Discover") }
        Text(status)
        Text("Connection is saved locally; mobile/FM Computer IP can change.")
        Text("Local discovery service: _fmcomputer._tcp.")
        Text("YouTube publishing: OFF")
        Text("FM Home approval: REQUIRED")
    }
}

suspend fun healthCheck(baseUrl: String): String = withContext(Dispatchers.IO) {
    try {
        val connection = URL(baseUrl.trimEnd('/') + "/health").openConnection() as HttpURLConnection
        connection.connectTimeout = 3000
        connection.readTimeout = 3000
        connection.requestMethod = "GET"
        val code = connection.responseCode
        connection.disconnect()
        if (code in 200..299) "FM Computer: ONLINE (HTTP $code)" else "FM Computer: ERROR (HTTP $code)"
    } catch (ex: Exception) {
        "FM Computer: OFFLINE — " + ex.javaClass.simpleName
    }
}



private fun discoverFmComputer(context: Context, callback: (String?) -> Unit) {
    val nsd = context.getSystemService(Context.NSD_SERVICE) as android.net.nsd.NsdManager
    var done = false
    lateinit var listener: android.net.nsd.NsdManager.DiscoveryListener

    fun finish(url: String?) {
        if (done) return
        done = true
        try { nsd.stopServiceDiscovery(listener) } catch (_: Exception) {}
        callback(url)
    }

    listener = object : android.net.nsd.NsdManager.DiscoveryListener {
        override fun onDiscoveryStarted(serviceType: String) = Unit
        override fun onServiceFound(serviceInfo: android.net.nsd.NsdServiceInfo) {
            nsd.resolveService(serviceInfo, object : android.net.nsd.NsdManager.ResolveListener {
                override fun onResolveFailed(info: android.net.nsd.NsdServiceInfo, errorCode: Int) = Unit
                override fun onServiceResolved(info: android.net.nsd.NsdServiceInfo) {
                    val host = info.host?.hostAddress ?: return
                    finish("http://" + host + ":" + info.port)
                }
            })
        }
        override fun onServiceLost(serviceInfo: android.net.nsd.NsdServiceInfo) = Unit
        override fun onDiscoveryStopped(serviceType: String) = Unit
        override fun onStartDiscoveryFailed(serviceType: String, errorCode: Int) = finish(null)
        override fun onStopDiscoveryFailed(serviceType: String, errorCode: Int) = Unit
    }

    nsd.discoverServices("_fmcomputer._tcp.", android.net.nsd.NsdManager.PROTOCOL_DNS_SD, listener)
}
