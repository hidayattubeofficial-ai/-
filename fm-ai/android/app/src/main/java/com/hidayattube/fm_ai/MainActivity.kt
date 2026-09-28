package com.hidayattube.fm_ai

import android.content.Context
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
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
        setContent { FmHomeAdminScreen(this) }
    }
}

private data class AdminOption(val title: String, val detail: String)

@Composable
fun FmHomeAdminScreen(context: Context) {
    val prefs = remember { context.getSharedPreferences("fm_ai_connection", Context.MODE_PRIVATE) }
    var baseUrl by remember {
        mutableStateOf(
            prefs.getString("fm_computer_url", "http://127.0.0.1:8080")
                ?: "http://127.0.0.1:8080"
        )
    }
    var status by remember { mutableStateOf("Not checked") }
    var checking by remember { mutableStateOf(false) }
    var discovering by remember { mutableStateOf(false) }
    var discoveryState by remember { mutableStateOf("Not checked") }
    var discoveredHost by remember { mutableStateOf<String?>(null) }
    var selected by remember { mutableStateOf("Dashboard") }
    val scope = rememberCoroutineScope()

    val options = listOf(
        AdminOption("Dashboard", "FM AI, FM Computer and runtime overview"),
        AdminOption("FM Computer", "Connection URL, LAN discovery and health check"),
        AdminOption("FM AI", "Survival AI runtime, local memory and recovery"),
        AdminOption("FM Home", "Approval and governance controls"),
        AdminOption("Ollama", "Local model/runtime status and model selection"),
        AdminOption("Memory", "Local memory storage and maintenance"),
        AdminOption("Logs", "Health, error and recovery logs"),
        AdminOption("Security", "Local-only access and security controls"),
        AdminOption("Recovery", "Recovery and restart controls"),
        AdminOption("Videos", "Content generation and review status"),
        AdminOption("YouTube", "Publishing control — permanently OFF by default"),
        AdminOption("Settings", "Intervals, paths and connection settings"),
        AdminOption("System Info", "CPU, RAM, storage and app information"),
        AdminOption("Audit Trail", "Approved and executed actions")
    )

    LazyColumn(
        modifier = Modifier.fillMaxSize().padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        item {
            Text("FM Home • Admin", style = MaterialTheme.typography.headlineMedium)
            Text("Survival Computer AI control center")
        }

        item { Text("Selected: $selected", style = MaterialTheme.typography.titleMedium) }

        if (selected == "Dashboard" || selected == "FM Computer") {
            item {
                OutlinedTextField(
                    value = baseUrl,
                    onValueChange = { baseUrl = it.trimEnd('/') },
                    label = { Text("FM Computer URL") },
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true
                )
            }
            item {
                Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    Button(enabled = !checking, onClick = {
                        prefs.edit().putString("fm_computer_url", baseUrl).apply()
                        checking = true
                        status = "Checking…"
                        scope.launch {
                            status = healthCheck(baseUrl)
                            checking = false
                        }
                    }) { Text("Check") }

                    OutlinedButton(enabled = !discovering, onClick = {
                        discovering = true
                        status = "Searching local network…"
                        discoveryState = "Searching…"
                        discoverFmComputer(context) { discovered ->
                            discovering = false
                            if (discovered != null) {
                                discoveredHost = discovered
                                discoveryState = "Ready"
                                baseUrl = discovered
                                prefs.edit().putString("fm_computer_url", discovered).apply()
                                status = "FM Computer found: $discovered"
                            } else {
                                discoveredHost = null
                                discoveryState = "Not found"
                                status = "FM Computer not found; enter its current LAN URL."
                            }
                        }
                    }) { Text(if (discovering) "Searching…" else "Auto Discover") }
                }
            }
            item { Text(status) }
            item {
                Card(modifier = Modifier.fillMaxWidth()) {
                    Column(
                        Modifier.padding(16.dp),
                        verticalArrangement = Arrangement.spacedBy(6.dp)
                    ) {
                        Text("LAN Discovery", style = MaterialTheme.typography.titleMedium)
                        Text("Service: _fmcomputer._tcp.")
                        Text("Discovery: $discoveryState")
                        Text("FM Computer: ${discoveredHost ?: "Not discovered"}")
                        Text("API: $baseUrl")
                        Text("Runtime: local only")
                    }
                }
            }
        }

        if (selected != "Dashboard" && selected != "FM Computer") {
            item {
                Card(modifier = Modifier.fillMaxWidth()) {
                    Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                        Text(selected, style = MaterialTheme.typography.titleLarge)
                        Text(options.first { it.title == selected }.detail)
                        if (selected == "YouTube") {
                            Text("Publishing: OFF")
                            Text("Human approval: REQUIRED")
                        }
                        if (selected == "FM Home") {
                            Text("Governance: approval required before protected actions")
                        }
                    }
                }
            }
        }

        item { Text("Admin Options", style = MaterialTheme.typography.titleLarge) }

        items(options) { option ->
            OutlinedButton(
                onClick = { selected = option.title },
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(
                    modifier = Modifier.fillMaxWidth(),
                    verticalArrangement = Arrangement.spacedBy(2.dp)
                ) {
                    Text(option.title)
                    Text(option.detail, style = MaterialTheme.typography.bodySmall)
                }
            }
        }

        item {
            Text("Discovery status is informational; no remote start/stop is exposed.")
            Text("Mobile IP can change; the saved URL and local discovery are used instead.")
            Text("Discovery service: _fmcomputer._tcp.")
            Text("YouTube publishing: OFF")
            Text("FM Home approval: REQUIRED")
        }
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
        if (code in 200..299) "FM Computer: ONLINE (HTTP $code)"
        else "FM Computer: ERROR (HTTP $code)"
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

    nsd.discoverServices(
        "_fmcomputer._tcp.",
        android.net.nsd.NsdManager.PROTOCOL_DNS_SD,
        listener
    )
}
