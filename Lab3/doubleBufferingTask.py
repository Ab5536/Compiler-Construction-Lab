import threading
import time

BUFFER_SIZE = 10  # Max characters per buffer

# Two buffers
buffer_A = []
buffer_B = []

# Shared variables
active_buffer = 'A'
lock = threading.Lock()
buffer_ready_event = threading.Event()
buffer_processed_event = threading.Event()
exit_event = threading.Event()

# Start with buffer processed (ready to fill)
buffer_processed_event.set()

# Global stack for processed data
processed_stack = []


def fill_buffer():
    """
    Producer thread: reads user input, fills active buffer, and switches between A/B
    """
    global active_buffer, buffer_A, buffer_B

    print("\n💡 Type your source code (type 'q' to quit):\n")

    while not exit_event.is_set():
        try:
            user_input = input("> ").strip()
            time.sleep(0.1)
        except EOFError:
            break

        # Quit condition
        if user_input.lower() == 'q' or not user_input:
            exit_event.set()
            buffer_ready_event.set()
            break

        # Break input into chunks of BUFFER_SIZE chars
        i = 0
        length = len(user_input)
        while i < length:
            chunk = user_input[i:i + BUFFER_SIZE]
            i += BUFFER_SIZE

            # Wait until consumer finishes processing previous buffer
            buffer_processed_event.wait()
            buffer_processed_event.clear()

            # Fill active buffer with chunk
            with lock:
                buffer = buffer_A if active_buffer == 'A' else buffer_B
                buffer.clear()
                buffer.extend(list(chunk))
                current_buffer = active_buffer

                # Switch buffer for next chunk
                active_buffer = 'B' if active_buffer == 'A' else 'A'

            print(f"[Producer] Filled Buffer {current_buffer} with {len(chunk)} chars")

            # Notify consumer that buffer is ready
            buffer_ready_event.set()
            time.sleep(0.1)  # Small delay for demo visibility


def process_data():
    """
    Consumer thread: processes the inactive buffer (splits into words)
    """
    global active_buffer, buffer_A, buffer_B, processed_stack

    while not exit_event.is_set():
        buffer_ready_event.wait()  # Wait for signal from producer
        buffer_ready_event.clear()

        if exit_event.is_set():
            break

        with lock:
            # Choose the buffer not currently active
            inactive_buffer = buffer_B if active_buffer == 'A' else buffer_A
            data = ''.join(inactive_buffer)

        # Process the data (split into words)
        if data:
            words = data.split()
            processed_stack.extend(words)  # ✅ Add to stack
            print(f"[Consumer] Processed {len(words)} words → {words}")

        time.sleep(0.3)  # Simulate processing time

        # Signal producer that processing is done
        buffer_processed_event.set()


# -------------------- Main Program -------------------- #
if __name__ == "__main__":
    print("=== Double Buffer Multithreading Demo ===")
    print("⚠️  Paste or type code on a single line")

    producer_thread = threading.Thread(target=fill_buffer, daemon=True)
    consumer_thread = threading.Thread(target=process_data, daemon=True)

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()

    # ✅ Display entire stack at the end
    print("\n✅ Program exited gracefully.")
    print(f"\n🧾 Processed Stack ({len(processed_stack)} words total):")
    print(processed_stack)

    # ✅ Save to output file
    try:
        with open("output.txt", "w", encoding="utf-8") as f:
            f.write("Processed Output (All Words)\n")
            f.write("=============================\n\n")
            for word in processed_stack:
                f.write(word + "\n")
        print("\n💾 Output saved successfully to 'output.txt'")
    except Exception as e:
        print(f"❌ Error saving file: {e}")
