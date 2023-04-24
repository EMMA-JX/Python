/**
 * Gaston Longhitano <gastonl@bu.edu> @ Boston University - Research
 *
 * This source code is licensed under the terms found in the
 * LICENSE file in the root directory of this source tree.
 */
package com.lalamoch

import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.ui.Modifier
import com.lalamoch.chat.conversation.ConversationContent
import com.lalamoch.chat.data.exampleUiState
import com.lalamoch.chat.theme.JetchatTheme


@Composable
internal fun ChatbotView(
    modifier: Modifier = Modifier,
) {
    CompositionLocalProvider(
    ) {
        JetchatTheme {
            ConversationContent(
                uiState = exampleUiState
            )
        }
    }
}