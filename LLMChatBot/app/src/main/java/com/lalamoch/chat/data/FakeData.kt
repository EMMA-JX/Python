/**
 * Gaston Longhitano <gastonl@bu.edu> @ Boston University - Research
 *
 * This source code is licensed under the terms found in the
 * LICENSE file in the root directory of this source tree.
 */
package com.lalamoch.chat.data

import com.lalamoch.R
import com.lalamoch.chat.conversation.ConversationUiState
import com.lalamoch.chat.conversation.Message

/**
 * This is a fake data class that is used to populate the UI with fake data.
 */
private val initialMessages = listOf(
    Message(
        "me",
        "What can I do to improve my workouts?",
        "8:07 AM"
    ),
    Message(
        "Bot",
        "Hi, ask me a question about your health and I'll try to answer it.",
        "8:01 AM"
    ),

)

/* This is for the autocomplete feature */
private val messageHints = listOf(
    "How many days did I run this month?",
    "How many steps did I walk this month?",
    "Did I run last week?",
    "What was my average heart rate today?",
    "How many steps did I walk the most in a day this month?"
)

/* build the UI state */
val exampleUiState = ConversationUiState(
    initialMessages = initialMessages,
    messageHints = messageHints
)
