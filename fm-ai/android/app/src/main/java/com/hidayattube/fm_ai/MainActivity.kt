package com.hidayattube.fm_ai

import android.content.Context
import android.os.Bundle
import android.Manifest
import android.content.pm.PackageManager
import androidx.activity.ComponentActivity
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.compose.setContent
import androidx.core.content.ContextCompat
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.clickable
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
import java.net.URI
import android.net.wifi.WifiManager

class MainActivity : ComponentActivity() {
    private var discoverAfterPermission: (() -> Unit)? = null
    private val nearbyPermissionLauncher =
        registerForActivityResult(ActivityResultContracts.RequestPermission()) { granted ->
            val action = discoverAfterPermission
            discoverAfterPermission = null
            if (granted) action?.invoke()
        }

    fun requestNearbyAndDiscover(action: () -> Unit) {
        if (android.os.Build.VERSION.SDK_INT < 33 ||
            ContextCompat.checkSelfPermission(this, Manifest.permission.NEARBY_WIFI_DEVICES) == PackageManager.PERMISSION_GRANTED
        ) action()
        else {
            discoverAfterPermission = action
            nearbyPermissionLauncher.launch(Manifest.permission.NEARBY_WIFI_DEVICES)
        }
    }

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
            prefs.getString("fm_computer_url", "") ?: ""
        )
    }
    var status by remember { mutableStateOf("Ready") }
    var checking by remember { mutableStateOf(false) }
    var discovering by remember { mutableStateOf(false) }
    var discoveryState by remember { mutableStateOf("Ready") }
    var discoveredHost by remember { mutableStateOf<String?>(null) }
    var discoveryMessage by remember { mutableStateOf("Tap Auto Discover to find FM Computer") }
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
                    label = { Text("FM Computer LAN URL") },
                    placeholder = { Text("http://192.168.x.x:8080") },
                    modifier = Modifier.fillMaxWidth(),
                    singleLine = true
                )
            }
            item {
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    Button(modifier = Modifier.weight(1f), enabled = !checking, onClick = {
                        val validation = validateBaseUrl(baseUrl)
                        if (validation != null) {
                            status = validation
                            return@Button
                        }
                        prefs.edit().putString("fm_computer_url", baseUrl.trimEnd('/')).apply()
                        checking = true
                        status = "Checking…"
                        scope.launch {
                            status = healthCheck(baseUrl)
                            checking = false
                        }
                    }) { Text("Check") }

                    Button(modifier = Modifier.weight(1f), enabled = !discovering, onClick = {
                        val activity = context as? MainActivity
                        activity?.requestNearbyAndDiscover {
                            discovering = true
                        status = "Searching local network…"
                        discoveryState = "Searching…"
                        discoveryMessage = "Looking for FM Computer on the local network"
                        discoverFmComputer(context) { discovered ->
                            discovering = false
                            if (discovered != null) {
                                discoveredHost = discovered
                                discoveryState = "Ready"
                                discoveryMessage = "FM Computer found via local discovery"
                                baseUrl = discovered
                                prefs.edit().putString("fm_computer_url", discovered).apply()
                                status = "FM Computer found: $discovered"
                            } else {
                                discoveredHost = null
                                discoveryState = "Not found"
                                discoveryMessage = "No FM Computer advertisement found"
                                status = "FM Computer not found; enter its current LAN URL."
                            }
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
                        Text(discoveryMessage, style = MaterialTheme.typography.bodySmall)
                        Text("FM Computer: ${discoveredHost ?: "Not discovered"}")
                        Text("API: ${baseUrl.ifBlank { "Not configured" }}")
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
            Button(
                modifier = Modifier.fillMaxWidth(),
                onClick = { selected = option.title; status = "Opened " + option.title }
            ) {
                Column(Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
                    Text(option.title, style = MaterialTheme.typography.titleMedium)
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

private fun validateBaseUrl(baseUrl: String): String? {
    if (baseUrl.isBlank()) return "FM Computer LAN URL is required. Use http://192.168.x.x:8080"
    if (!isValidBaseUrl(baseUrl)) return "Invalid LAN URL. Use http://192.168.x.x:8080 (not 127.0.0.1)."
    return null
}

private fun isValidBaseUrl(baseUrl: String): Boolean {
    return try {
        val uri = URI(baseUrl.trimEnd('/'))
        val host = uri.host
        (uri.scheme.equals("http", true) || uri.scheme.equals("https", true)) &&
            !host.isNullOrBlank() && !host.equals("127.0.0.1") &&
            !host.equals("localhost", true) && !host.equals("0.0.0.0") &&
            uri.query == null && uri.fragment == null
    } catch (_: Exception) { false }
}

suspend fun healthCheck(baseUrl: String): String = withContext(Dispatchers.IO) {
    val validation = validateBaseUrl(baseUrl)
    if (validation != null) return@withContext validation
    try {
        val connection = URI(baseUrl.trimEnd('/') + "/health").toURL().openConnection() as HttpURLConnection
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
    val wifi = context.applicationContext.getSystemService(Context.WIFI_SERVICE) as WifiManager
    val multicastLock = wifi.createMulticastLock("fmcomputer-discovery").apply { setReferenceCounted(false) }
    var done = false
    lateinit var listener: android.net.nsd.NsdManager.DiscoveryListener

    fun finish(url: String?) {
        if (done) return
        done = true
        try { nsd.stopServiceDiscovery(listener) } catch (_: Exception) {}
        try { if (multicastLock.isHeld) multicastLock.release() } catch (_: Exception) {}
        callback(url)
    }

    listener = object : android.net.nsd.NsdManager.DiscoveryListener {
        override fun onDiscoveryStarted(serviceType: String) = Unit
        override fun onServiceFound(serviceInfo: android.net.nsd.NsdServiceInfo) {
            nsd.resolveService(serviceInfo, object : android.net.nsd.NsdManager.ResolveListener {
                override fun onResolveFailed(info: android.net.nsd.NsdServiceInfo, errorCode: Int) = Unit
                override fun onServiceResolved(info: android.net.nsd.NsdServiceInfo) {
                    val host = info.host?.hostAddress ?: return
                    if (host.contains(":")) return
                    val url = "http://" + host + ":" + info.port
                    Thread {
                        val reachable = try {
                            val connection = URI(url + "/health").toURL().openConnection() as HttpURLConnection
                            connection.connectTimeout = 2500
                            connection.readTimeout = 2500
                            connection.responseCode in 200..299
                        } catch (_: Exception) { false }
                        if (reachable) android.os.Handler(android.os.Looper.getMainLooper()).post { finish(url) }
                    }.start()
                }
            })
        }
        override fun onServiceLost(serviceInfo: android.net.nsd.NsdServiceInfo) = Unit
        override fun onDiscoveryStopped(serviceType: String) = Unit
        override fun onStartDiscoveryFailed(serviceType: String, errorCode: Int) = finish(null)
        override fun onStopDiscoveryFailed(serviceType: String, errorCode: Int) = Unit
    }

    try {
        multicastLock.acquire()
        nsd.discoverServices("_fmcomputer._tcp.", android.net.nsd.NsdManager.PROTOCOL_DNS_SD, listener)
    } catch (_: Exception) {
        finish(null)
        return
    }
    android.os.Handler(android.os.Looper.getMainLooper()).postDelayed({ finish(null) }, 8000)
}
