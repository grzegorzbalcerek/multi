package cmd

import (
	"github.com/spf13/cobra"

	"github.com/grzegorzbalcerek/mvnlib"
)


type JarsDownloadFlags struct {
  OutDir string
  Verbose bool
  Par int
}

var jarsDownloadFlags = JarsDownloadFlags{}

// downloadCmd represents the download command
var jarsDownloadCmd = &cobra.Command{
	Use:   "download",
	Short: "download dependent jars",
	Long: `download dependent jars

Example:
gmvn jars download --group dev.zio --artifact zio-test_2.13 --version 1.0.15 -outdir lib -verbose`,
	Run: func(cmd *cobra.Command, args []string) {
		options := mvnlib.Options{
            Repo: rootFlags.Repo,
            Recursive: rootFlags.Recursive,
            GroupId: jarsFlags.Group,
            ArtifactId: jarsFlags.Artifact,
            Version: jarsFlags.Version,
            Parallel: jarsDownloadFlags.Par,
            OutputDir: jarsDownloadFlags.OutDir}
		mvnlib.Download(options)
	},
}

func init() {
	jarsCmd.AddCommand(jarsDownloadCmd)
	jarsDownloadCmd.Flags().StringVarP(&jarsDownloadFlags.OutDir, "outdir", "o", ".", "output directory")
	jarsDownloadCmd.Flags().BoolVar(&jarsDownloadFlags.Verbose, "verbose", false, "print additional information")
	jarsDownloadCmd.Flags().IntVarP(&jarsDownloadFlags.Par, "par", "p", 1, "number of parallel goroutines; should be 1 or more")
}
