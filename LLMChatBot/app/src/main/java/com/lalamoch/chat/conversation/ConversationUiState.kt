/**
 * Gaston Longhitano <gastonl@bu.edu> @ Boston University - Research
 *
 * This source code is licensed under the terms found in the
 * LICENSE file in the root directory of this source tree.
 */
package com.lalamoch.chat.conversation

import androidx.compose.runtime.Immutable
import androidx.compose.runtime.toMutableStateList
import com.lalamoch.R

/**
 * The state of the conversation screen.
 */
class ConversationUiState(
    initialMessages: List<Message>,
    messageHints: List<String>
) {
    private val _messages: MutableList<Message> = initialMessages.toMutableStateList()
    private val _messagesHints: MutableList<String> = messageHints.toMutableStateList()
    val messages: List<Message> = _messages
    val messagesHints: List<String> = _messagesHints

    fun addMessage(msg: Message) {
        _messages.add(0, msg) // Add to the beginning of the list
    }

    // This is for the autocomplete feature
    fun addMessageHint(hint: String) {
        _messagesHints.add(0, hint)
    }
}

@Immutable
data class Message(
    val author: String,
    val content: String,
    val timestamp: String,
    val image: Int? = null,
    val audio: Int? = null,
    val authorImage: Int = if (author == "me") R.drawable.gaston else R.drawable.bot
)
