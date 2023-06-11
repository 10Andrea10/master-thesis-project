import {spawn} from 'child_process';
import {ComputationResult} from '../typings/services';
import { readFileSync, rmSync } from 'fs';

export class ZokratesInteractor {
  private readonly workDir: string = './src/zokrates';

  /**
   * Computes the rollup proof spawning a zokrates process.
   * @param inputs The zokrates inputs properly formatted.
   * @returns The rollup proof execution.
   */
  async execute(inputs: string): Promise<ComputationResult> {
    return new Promise<ComputationResult>(resolveCallback => {
      const proc = spawn('zokrates', ['compute-witness', '--abi', '--stdin'], {
        cwd: this.workDir,
      });

      console.log(inputs.toString());

      proc.stdin.write(inputs);
      proc.stdin.end();

      proc.stdout.on('data', this.printStdout);
      proc.on('error', this.printError);
      proc.on('close', code => {
        this.printExitCode(code);
        if (code == 0) {
          this.proofGeneration(resolveCallback);
        } else {
          resolveCallback({
            success: false,
            error:
              'Error executing zokrates compute-witness with inputs: ' + inputs,
          });
        }
      });
    });
  }

  private proofGeneration(resolveCallback: (value: ComputationResult) => void) {
    const proc = spawn('zokrates', ['generate-proof', '-s', 'gm17'], {
      cwd: this.workDir,
    });
    proc.stdout.on('data', this.printStdout);
    proc.stderr.on('data', this.printStderr);
    proc.on('error', this.printError);
    proc.on('close', code => {
      this.printExitCode(code);
      if (code == 0) {
        resolveCallback({
          success: true,
          result: this.readProof(),
        });
      } else {
        resolveCallback({
          success: false,
          error: 'Error executing zokrates generate-proof',
        });
      }
    });
  }

  private readProof (): string {
    const proof = readFileSync(this.workDir + '/proof.json', 'utf8');
    rmSync(this.workDir + '/proof.json');
    rmSync(this.workDir + '/witness');
    rmSync(this.workDir + '/out.wtns');
    return proof;
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
