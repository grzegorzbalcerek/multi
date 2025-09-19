package cmd

import (
	"os"

	"github.com/spf13/cobra"
)

type RootFlags struct {
  Repo string
  Recursive bool
}

var rootFlags = RootFlags{}


// rootCmd represents the base command when called without any subcommands
var rootCmd = &cobra.Command{
	Use:   "gmvn",
	Short: "A tool for working with maven dependencies",
	Long: `A tool for working with maven dependencies`,
}

// Execute adds all child commands to the root command and sets flags appropriately.
// This is called by main.main(). It only needs to happen once to the rootCmd.
func Execute() {
	err := rootCmd.Execute()
	if err != nil {
		os.Exit(1)
	}
}

func init() {
	rootCmd.PersistentFlags().StringVar(&rootFlags.Repo, "repo", "https://repo1.maven.org/maven2", "repository url")
	rootCmd.PersistentFlags().BoolVarP(&rootFlags.Recursive, "recursive", "r", true, "recursive flag")
// 	rootCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
}


