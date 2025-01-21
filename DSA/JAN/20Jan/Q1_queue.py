# // Question: Sindhu attends online classes. She is unable to complete after
# // class assignments Sometimes she misses the due date and
# // then that assignment gets marked as turned in late. She is
# // unable to think how to manage assignments. To help her, write
# // a python program and create a queue data structure so that
# // she can enqueue ( add ) new assignments inside the queue.
# // Also, create a peek() method which can help her in getting the
# // oldest assignment she added in the queue. Create a dequeue
# // method that can help her in removing the peek() assessment
# // after she completes it. Also, create a method isEmpty() so that
# // she can check whether she left with any assignment or not.
# // Inclass Challenge 1 -Assignment Queue

class AssignmentQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, assignment):
        """Add a new assignment to the queue."""
        self.queue.append(assignment)
        print(f"Assignment '{assignment}' added to the queue.")

    def peek(self):
        """Get the oldest assignment in the queue."""
        if not self.isEmpty():
            return self.queue[0]
        else:
            print("No assignments left in the queue!")
            return None

    def dequeue(self):
        """Remove the oldest assignment from the queue."""
        if not self.isEmpty():
            completed_assignment = self.queue.pop(0)
            print(f"Assignment '{completed_assignment}' completed and removed from the queue.")
        else:
            print("No assignments to complete!")

    def isEmpty(self):
        """Check if the queue is empty."""
        return len(self.queue) == 0

# Example usage:
if __name__ == "__main__":
    sindhu_assignments = AssignmentQueue()

    # Add assignments to the queue
    sindhu_assignments.enqueue("Math Homework")
    sindhu_assignments.enqueue("Science Project")
    sindhu_assignments.enqueue("English Essay")

    # Peek at the oldest assignment
    print(f"Oldest Assignment: {sindhu_assignments.peek()}")

    # Complete assignments
    sindhu_assignments.dequeue()
    sindhu_assignments.dequeue()

    # Check if the queue is empty
    print("Is the queue empty?", sindhu_assignments.isEmpty())

    # Peek again after completing some assignments
    print(f"Oldest Assignment: {sindhu_assignments.peek()}")

    # Complete the remaining assignment
    sindhu_assignments.dequeue()

    # Check if the queue is empty
    print("Is the queue empty?", sindhu_assignments.isEmpty())




