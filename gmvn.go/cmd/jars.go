package cmd

import (

	"github.com/spf13/cobra"
)

type JarsFlags struct {
  Group string
  Artifact string
  Version string
}

var jarsFlags = JarsFlags{}

// jarsCmd represents the jars command
var jarsCmd = &cobra.Command{
	Use:   "jars",
	Short: "jars command",
	Long: `jars command`,
}

func init() {
	rootCmd.AddCommand(jarsCmd)

	jarsCmd.PersistentFlags().StringVarP(&jarsFlags.Group, "group", "g", "", "maven group id (required)")
	jarsCmd.MarkPersistentFlagRequired("group")
	jarsCmd.PersistentFlags().StringVarP(&jarsFlags.Artifact, "artifact", "a", "", "maven artifact id (required)")
	jarsCmd.MarkPersistentFlagRequired("artifact")
	jarsCmd.PersistentFlags().StringVarP(&jarsFlags.Version, "version", "v", "", "maven version (required)")
	jarsCmd.MarkPersistentFlagRequired("version")
	// jarsCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
}
