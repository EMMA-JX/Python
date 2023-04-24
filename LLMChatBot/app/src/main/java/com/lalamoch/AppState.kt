/**
 * Gaston Longhitano <gastonl@bu.edu> @ Boston University - Research
 *
 * This source code is licensed under the terms found in the
 * LICENSE file in the root directory of this source tree.
 */
package com.lalamoch

import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import com.lalamoch.model.Model

@Composable
fun rememberAppState(
    llm: Nothing? = null
) = remember(llm) {
    AppState(llm)
}

class AppState(
    var llm: Model? = null,
) {
    init {
        startLLMService()
    }

    fun startLLMService() {
       //TODO: start LLM service
        llm = Model()
    }
}