import std/cmdline, std/osproc

proc main() =
  var firstParam = paramStr(1)

  # error of executeShellCmd
  var error: int = 0 

  case firstParam:
    of "-h", "--help":
      echo "Usage: notetaker [command]"
      echo "Commands:"
      echo "  -h, --help    Show this help message and exit"
      echo "  -b, --build   Build and run the project"
      echo "  -sh, --shell  Open the shell"
      echo "  -r, --run     Run the project"
      echo "  -shr, --shell react Open a shell in the react container"
      echo "  -d, --down    Stop the project"
    of "-b", "--build":
      error = execCmd("docker compose up --build")
    of "-sh", "--shell":
      error = execCmd("docker exec -it notetaker-app-1 /bin/bash")
    of "-r", "--run":
      error = execCmd("docker compose up")
    of "-shr", "--shell-react":
      error = execCmd("docker exec -it notetaker-react-app-1 /bin/bash")
    of "-d", "--down":
      error = execCmd("docker compose down")
    else:
      echo "Invalid command. Use -h or --help to see the available commands"

  if error != 0:
    echo "An error occurred while executing the command"
    echo error


main()
