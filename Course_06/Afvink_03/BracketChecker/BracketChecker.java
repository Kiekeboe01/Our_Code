package Course_06.Afvink_03.BracketChecker;

import java.io.IOException;
public class BracketChecker {



    public static void check(String input) {
        int stackSize = input.length();
        Stack theStack = new Stack(stackSize);

        for (int j = 0; j < input.length(); j++) {
            char ch = input.charAt(j);
            switch (ch) {
                case '{': // opening symbols
                case '[':
                case '(':
                    theStack.push(ch); // push them
                    break;

                case '}': // closing symbols
                case ']':
                case ')':
                    if (!theStack.isEmpty()) // if stack not empty,
                    {
                        char chx = theStack.pop(); // pop and check
                        if ((ch == '}' && chx != '{') || (ch == ']' && chx != '[') || (ch == ')' && chx != '(')) {
                            System.out.println("Error: " + ch + " at " + j);
                        }
                    } else // prematurely empty
                    {
                        System.out.println("Error: " + ch + " at " + j);
                    }
                    break;
                default: // no action on other characters
                    break;
            }
        }
        if (!theStack.isEmpty()) {
            System.out.println("Error: missing right delimiter");
        }
    }

    public static void main(String[] args) throws IOException {
        System.out.println("\n\nOpdracht_01");
        String invoer = "{(9+9)[432]{{(329321}}";
        System.out.println(invoer);
        check(invoer);
    }
}