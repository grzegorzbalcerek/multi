package cmd

import (
	"github.com/spf13/cobra"

 	"github.com/grzegorzbalcerek/mvnlib"
)

// listCmd represents the list command
var listCmd = &cobra.Command{
	Use:   "list",
	Short: "list dependent jars",
	Long: `list dependent jars

Example:
gmvn jars list --group dev.zio --artifact zio-test_2.13 --version 1.0.15 -outdir lib -verbose`,
	Run: func(cmd *cobra.Command, args []string) {
		options := mvnlib.Options{
            Repo: rootFlags.Repo,
            Recursive: rootFlags.Recursive,
            GroupId: jarsFlags.Group,
            ArtifactId: jarsFlags.Artifact,
            Version: jarsFlags.Version}
		mvnlib.List(options)
	},
}

func init() {
	jarsCmd.AddCommand(listCmd)
}
