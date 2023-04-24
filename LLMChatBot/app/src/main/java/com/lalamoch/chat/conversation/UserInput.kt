/**
 * Gaston Longhitano <gastonl@bu.edu> @ Boston University - Research
 *
 * This source code is licensed under the terms found in the
 * LICENSE file in the root directory of this source tree.
 *
 * -------------------------------------------------------------
 * NOTE:
 * This file contains code from the Android Open Source Project
 * Copyright 2020 The Android Open Source Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */


package com.lalamoch.chat.conversation
import androidx.compose.animation.*
import androidx.compose.foundation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.ClickableText
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.focus.focusTarget
import androidx.compose.ui.focus.onFocusChanged
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.semantics.SemanticsPropertyKey
import androidx.compose.ui.semantics.SemanticsPropertyReceiver
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.TextRange
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.lalamoch.R
import java.lang.Integer.min

enum class InputSelector {
    NONE,
    SUGGESTIONS,
}

@Preview
@Composable
fun UserInputPreview() {
    UserInput(onMessageSent = {})
}

@OptIn(ExperimentalFoundationApi::class)
@Composable
fun UserInput(
    onMessageSent: (String) -> Unit,
    modifier: Modifier = Modifier,
    resetScroll: () -> Unit = {},
    messagesHints: List<String> = emptyList(),
    ) {
    var currentInputSelector by rememberSaveable { mutableStateOf(InputSelector.NONE) }
    val dismissKeyboard = { currentInputSelector = InputSelector.NONE }
    var textState by rememberSaveable(stateSaver = TextFieldValue.Saver) {
        mutableStateOf(TextFieldValue())
    }

    // Used to decide if the keyboard should be shown
    var textFieldFocusState by remember { mutableStateOf(false) }

    Surface(tonalElevation = 2.dp) {
        Column(modifier = modifier) {
            displayHints(textState.text, messagesHints)?.let { it ->
                SelectorExpanded(
                    onCloseRequested = dismissKeyboard,
                    onTextAdded = { textState = textState.addText(it) },
                    currentSelector = currentInputSelector,
                    messagesHints = it
                )
            }

            UserInputText(
                textFieldValue = textState,
                onTextChanged = {
                    textState = it
                    currentInputSelector = if (displayHints(it.text, messagesHints)?.isNotEmpty() == true) {
                        InputSelector.SUGGESTIONS
                    } else {
                        InputSelector.NONE
                    }
                },
                // Only show the keyboard if there's no input selector and text field has focus
                keyboardShown = currentInputSelector == InputSelector.NONE && textFieldFocusState,
                // Close extended selector if text field receives focus
                onTextFieldFocused = { focused ->
                    if (focused) {
                        currentInputSelector = InputSelector.NONE
                        resetScroll()
                    }
                    textFieldFocusState = focused
                },
                focusState = textFieldFocusState,
                onMessageSent = {
                    onMessageSent(textState.text)
                    // Reset text field and close keyboard
                    textState = TextFieldValue()
                    // Move scroll to bottom
                    resetScroll()
                    dismissKeyboard()
                }
            )
        }
    }
}

/**
 * Insert the suggested text at the current cursor position and move the cursor to the end of the inserted text without duplication
 */
private fun TextFieldValue.addText(newString: String): TextFieldValue {
    val newSelection = TextRange(
        start = newString.length,
        end = newString.length
    )
    return this.copy(text = newString, selection = newSelection)
}

@Composable
private fun SelectorExpanded(
    currentSelector: InputSelector,
    onCloseRequested: () -> Unit,
    onTextAdded: (String) -> Unit,
    messagesHints: List<String> = emptyList(),
) {
    if (currentSelector == InputSelector.NONE) return
    // Request focus to force the TextField to lose it
    val focusRequester = FocusRequester()

    Surface(tonalElevation = 8.dp) {
        //TODO: Here is where we can add more selectors based on the user input text (GL)
        when (currentSelector) {
            InputSelector.SUGGESTIONS -> MessagesHintSelector(onTextAdded, focusRequester,onCloseRequested, messagesHints)
            else -> { throw NotImplementedError() }
        }
    }
}

@Composable
fun MessagesHintSelector(
    onTextAdded: (String) -> Unit,
    focusRequester: FocusRequester,
    onCloseRequested: () -> Unit,
    messagesHints: List<String> = emptyList(),
) {
    var selected by remember { mutableStateOf("") }
    Column(
        modifier = Modifier
            .focusRequester(focusRequester) // Requests focus when the Hints selector is displayed
            // Make the Hints selector focusable so it can steal focus from TextField
            .focusTarget()
            .fillMaxWidth()

    ) {
        messagesHints.forEach { suggestion ->
            ClickableText(AnnotatedString(suggestion),
                modifier = Modifier.padding(8.dp),
              //  style = MaterialTheme.typography.labelMedium,
                onClick = {
                selected = suggestion
                onTextAdded(suggestion)
                onCloseRequested()
            })
        }
    }
}

val KeyboardShownKey = SemanticsPropertyKey<Boolean>("KeyboardShownKey")
var SemanticsPropertyReceiver.keyboardShownProperty by KeyboardShownKey

/**
 * Resolve the list of hints to display based on the current text input
 */
private fun displayHints(text: String, hints: List<String>): List<String>? {
    // Cache to avoid recomposing the list of hints every time the user types a new character (GL)
    val cache: MutableMap<String, List<String>> = mutableMapOf()

    if (cache.containsKey(text)) {
        return cache[text]
    }

    if (text.isEmpty()) return emptyList()
    if (text.length >= 3 && hints.isNotEmpty()) {
        val results = hints.filter { it.contains(text, true) }
        cache[text] = results
        // Return at most 5 results
        return results.subList(0, min(results.size, 5))
    }

    return emptyList()
}

@ExperimentalFoundationApi
@Composable
private fun UserInputText(
    keyboardType: KeyboardType = KeyboardType.Text,
    onTextChanged: (TextFieldValue) -> Unit,
    textFieldValue: TextFieldValue,
    keyboardShown: Boolean,
    onTextFieldFocused: (Boolean) -> Unit,
    focusState: Boolean,
    onMessageSent: () -> Unit,
) {
    val a11ylabel = stringResource(id = R.string.textfield_desc)
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .height(80.dp)
            .semantics {
                contentDescription = a11ylabel
                keyboardShownProperty = keyboardShown
            },
        horizontalArrangement = Arrangement.End
    ) {
        Surface(
            modifier = Modifier.fillMaxSize()
        ) {
            Box(
                modifier = Modifier
                    //.height(50.dp)
                    .weight(1f)
                    .align(Alignment.Bottom)
                  //  .align(Alignment.CenterVertically)
            ) {
                var lastFocusState by remember { mutableStateOf(false) }

                Row() {
                    Box() {
                        BasicTextField(
                            value = textFieldValue,
                            onValueChange = { onTextChanged(it) },
                            modifier = Modifier
                                .fillMaxSize(0.8F)
                                .padding(start = 32.dp, top = 17.dp)
                                .height(50.dp)
                                .onFocusChanged { state ->
                                    if (lastFocusState != state.isFocused) {
                                        onTextFieldFocused(state.isFocused)
                                    }
                                    lastFocusState = state.isFocused
                                },
                            keyboardOptions = KeyboardOptions(
                                keyboardType = keyboardType,
                                imeAction = ImeAction.Send

                            ),
                            maxLines = 2,
                            cursorBrush = SolidColor(LocalContentColor.current),
                            textStyle = LocalTextStyle.current.copy(color = LocalContentColor.current)
                        )
                        val disableContentColor =
                            MaterialTheme.colorScheme.onSurfaceVariant
                        if (textFieldValue.text.isEmpty() && !focusState) {
                            Text(
                                modifier = Modifier
                                    // .align(Alignment.)
                                    .padding(start = 32.dp, top = 17.dp, bottom = 5.dp),
                                text = stringResource(id = R.string.textfield_hint),
                                style = MaterialTheme.typography.bodyLarge.copy(color = disableContentColor)
                            )
                        }
                    }

                    val sendMessageEnabled = textFieldValue.text.isNotEmpty()
                    val border = if (!sendMessageEnabled) {
                        BorderStroke(
                            width = 1.dp,
                            color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.3f)
                        )
                    } else {
                        null
                    }

                    val disabledContentColor = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.3f)

                    val buttonColors = ButtonDefaults.buttonColors(
                        disabledContainerColor = Color.Transparent,
                        disabledContentColor = disabledContentColor
                    )

                    // Send button
                    Button(
                        modifier = Modifier
                            .fillMaxWidth()
                            //.fillMaxSize()
                            .padding(end = 3.dp, top = 5.dp),
                        enabled = sendMessageEnabled,
                        onClick = onMessageSent,
                        colors = buttonColors,
                        border = border,
                        contentPadding = PaddingValues(0.dp)
                    ) {
                        Text(
                            stringResource(id = R.string.send),
                            modifier = Modifier.padding(horizontal = 16.dp)
                        )
                    }
                }
            }
        }
    }
}