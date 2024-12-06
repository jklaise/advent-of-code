# Read and parse
{:ok, content} = File.read("input.txt")

reports =
  content
  |> String.split("\n", trim: true)
  |> Enum.map(fn line ->
    line
    |> String.split(" ")
    |> Enum.map(&String.to_integer/1)
  end)

# IO.inspect(reports, charlists: :as_lists)

defmodule Eval do
  def is_safe?(line) do
    diffs =
      Eval.get_diffs(line)

    diffs |> Enum.all?(fn x -> x > 0 and x < 4 end) or
      diffs |> Enum.all?(fn x -> x < 0 and x > -4 end)
  end

  def get_diffs(line) do
    line
    |> Enum.zip(tl(line))
    |> Enum.map(fn {a, b} -> b - a end)
  end

  def exclude_each(line) do
    line
    |> Enum.with_index()
    |> Enum.map(fn {_, index} -> List.delete_at(line, index) end)
  end

  def is_safe2?(line) do
    exclude_each(line)
    |> Enum.any?(&is_safe?/1)
  end
end

# Part 1
number_safe =
  reports
  |> Enum.map(&Eval.is_safe?/1)
  |> Enum.count(fn x -> x == true end)

IO.inspect(number_safe)

number_safe2 =
  reports
  |> Enum.map(&Eval.is_safe2?/1)
  |> Enum.count(fn x -> x == true end)

IO.inspect(number_safe2)
