import argparse
import os
import json

def create_parser():
    parser = argparse.ArgumentParser(description="Extract keywords from markdown files.")
    parser.add_argument(
        "-i", "--input_path", type=str, default="data", help="Input markdown files."
    )
    parser.add_argument(
        "-o", "--output_path", type=str, default="keyword/keywords.jsonl", help="Output file path for extracted keywords."
    )
    parser.add_argument(
        "-m", "--method", type=str, choices=["textrank", "bert", "llm"], default="textrank",
        help="Method to use for keyword extraction: textrank, bert, or llm."
    )

    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()
    
    # load input_path
    if not os.path.exists(args.input_path):
        print(f"Input directory {args.input_path} does not exist.")
        return
    with open(args.input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    if args.method == "textrank":
        from textrank import extract_keywords
        res = extract_keywords(text)
        res = {"keywords": res}
        
    elif args.method == "bert":
        from bert import extract_keywords_bert
        res = extract_keywords_bert(text)
        res = {"keywords": res}
        
    elif args.method == "llm":
        from llm import extract_keywords_llm
        import asyncio
        res = asyncio.run(extract_keywords_llm(text, args.input_path))
    else:
        print("Invalid method specified. Use 'textrank', 'bert', or 'llm'.")
        exit(1)
        
    # Save results to output file
    args.output_path = os.path.abspath(args.output_path)
    if not os.path.exists(os.path.dirname(args.output_path)):
        os.makedirs(os.path.dirname(args.output_path))
    with open(args.output_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(res, ensure_ascii=False) + "\n")
        
    print(f"Keywords extracted and saved to {args.output_path}")
        
if __name__ == "__main__":
    main()