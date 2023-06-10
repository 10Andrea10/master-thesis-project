import {spawn} from 'child_process';

export class ZokratesInteractor {
  async execute(inputs: string): Promise<string> {
    return new Promise(resolve => {
      const proc = spawn('zokrates', ['--version']);
      proc.stdout.on('data', this.printStdout);
      proc.stderr.on('data', this.printStderr);
      proc.on('error', this.printError);
      proc.on('close', code => {
        this.printExitCode(code);
      });
      // TODO: return result
    });
  }

  private printStdout = (data: string) => {
    console.log(`stdout: ${data}`);
  };

  private printStderr = (data: string) => {
    console.log(`stderr: ${data}`);
  };

  private printError = (error: Error) => {
    console.log(`error: ${error.message}`);
  };

  private printExitCode = (code: number | null) => {
    console.log(`child process exited with code ${code}`);
  };
}
