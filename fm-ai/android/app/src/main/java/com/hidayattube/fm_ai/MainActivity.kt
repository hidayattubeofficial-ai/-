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
    var baseUrl by remember { mutableStateOf("http://127.0.0.1:8080") }
    var status by remember { mutableStateOf("Not checked") }
    var checking by remember { mutableStateOf(false) }
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
            checking = true
            status = "Checking…"
            scope.launch {
                status = healthCheck(baseUrl)
                checking = false
            }
        }) { Text("Check FM Computer") }
        Text(status)
        Text("IP-independent: change the FM Computer URL when the network address changes.")
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
